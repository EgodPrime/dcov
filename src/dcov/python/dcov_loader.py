import sys
from importlib import machinery
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import SourceFileLoader
from importlib.util import find_spec
from pathlib import Path
from types import CodeType, FunctionType
from typing import Optional

from dcov.python.bitmap_manager import BitmapManager
from dcov.python.dcov_monitor import event_map, register_by_cov_type


def _collect_code_objects(module, source_path: Path) -> set:
    """Collect top-level live CodeType objects from an already-loaded module.

    Returns top-level code objects (functions/classes defined directly in this
    module's __dict__).  These are the same objects that the interpreter will
    execute, so instrumenting them with sys.monitoring.set_local_events() has
    an immediate effect.

    Only collects top-level code objects -- instrument_code() will recurse
    into co.co_consts, so avoiding double-recursion.

    Only code objects whose co_filename is under source_path are included, so
    that imported/dependency code is excluded.

    NOTE: We deliberately do NOT use loader.get_code() to recompile, because
    that produces NEW code objects equal but not identical to the originals.
    sys.monitoring.set_local_events() operates by object identity.
    """
    import types

    collected = set()
    seen = set()

    def _scan_obj(obj):
        oid = id(obj)
        if oid in seen:
            return
        seen.add(oid)

        # Extract __code__ if present (functions, methods).
        code = getattr(obj, "__code__", None)
        if isinstance(code, types.CodeType):
            # Only collect top-level code objects -- let instrument_code
            # handle nested ones.  Filter by co_filename to avoid
            # instrumenting code that belongs to a different library.
            try:
                co_path = Path(code.co_filename).resolve()
            except (ValueError, TypeError, OSError):
                co_path = None

            if co_path is not None and co_path.is_relative_to(source_path):
                collected.add(code)

        # Recurse into __dict__ to find nested functions/classes, but SKIP
        # ModuleType instances found inside -- those are imported dependencies
        # whose code objects should not be instrumented.
        if hasattr(obj, "__dict__"):
            for v in obj.__dict__.values():
                if isinstance(v, types.ModuleType):
                    continue  # don't descend into dependency modules
                _scan_obj(v)

    _scan_obj(module)
    return collected


def instrument_code(co: CodeType, events):
    # print(f"Instrumenting on:{co.co_name}--from--{co.co_filename}")
    # print(f"Instrumenting code: {co.co_filename}-{co.co_firstlineno}")
    if isinstance(co, FunctionType):
        co = co.__code__
    for event in events:
        sys.monitoring.set_local_events(sys.monitoring.COVERAGE_ID, co, event)
    for c in co.co_consts:
        if isinstance(c, CodeType):
            instrument_code(c, events)


class DcovLoader(Loader):
    def __init__(self, orig_loader: SourceFileLoader, cov_type: str):
        self.orig_loader = orig_loader
        self.events = event_map[cov_type]

    def create_module(self, spec):
        mod = self.orig_loader.create_module(spec)
        return mod

    def get_code(self, name):
        return self.orig_loader.get_code(name)

    def exec_module(self, module):
        try:
            code = self.orig_loader.get_code(module.__name__)
            instrument_code(code, self.events)
            exec(code, module.__dict__)
        except Exception as e:
            self.orig_loader.exec_module(module)


class DcovMetaPathFinder(MetaPathFinder):
    def __init__(self, class_name):
        self.sources = []
        self.class_name = class_name

    def find_spec(self, fullname, path, target=None):
        for f in sys.meta_path:

            if isinstance(f, DcovMetaPathFinder):
                continue

            if not hasattr(f, "find_spec"):
                continue

            spec = f.find_spec(fullname, path, target)
            if spec is None or spec.loader is None or spec.origin is None:
                continue

            # can't instrument extension files
            if isinstance(
                spec.loader, (machinery.ExtensionFileLoader, machinery.BuiltinImporter)
            ):
                return spec

            filename = Path(spec.origin).resolve()
            if filename.suffix in (".pyd", ".so"):
                return spec

            # if filename.suffix not in (".py", ".pyi"):
            #     return spec

            if any(filename.is_relative_to(s) for s in self.sources):
                spec.loader = DcovLoader(spec.loader, self.class_name)

            return spec

        return None


class LoaderWrapper:
    def __init__(
        self, bm: BitmapManager, cov_type="line", library_name: Optional[str] = None
    ):
        self.class_name = cov_type
        if cov_type == "edge":
            hit_func = bm.add_edge
        else:
            hit_func = bm.set_bit
        register_by_cov_type(cov_type, hit_func, bm.bitmap_size)
        self.mpf = DcovMetaPathFinder(cov_type)
        self.default_library_name = library_name

        if library_name is not None:
            spec = find_spec(library_name)
            if spec is None or spec.origin is None:
                raise ImportError(f"Cannot find library {library_name}")
            self.add_source(spec.origin, library_name=library_name)

    def __enter__(self):
        sys.meta_path.insert(0, self.mpf)
        return self

    def __exit__(self, *args) -> None:
        i = 0
        while i < len(sys.meta_path):
            if sys.meta_path[i] is self.mpf:
                sys.meta_path.pop(i)
                break
            i += 1

    def _instrument_already_loaded(
        self, source_path: Path, library_name: str
    ) -> None:
        """Instrument modules that are already in sys.modules under the given source.

        When a library has been imported before LoaderWrapper.__enter__, the
        MetaPathFinder never gets a chance to intercept.  This method finds those
        cached sub-modules and instruments their code objects directly via
        sys.monitoring.set_local_events().
        """
        events = event_map.get(self.class_name, [])
        if not events:
            return

        for mod_name, mod in sys.modules.items():
            # Only consider the target library and its sub-modules
            if mod_name != library_name and not mod_name.startswith(
                library_name + "."
            ):
                continue

            mod_file = getattr(mod, "__file__", None)
            if mod_file is None:
                continue

            try:
                mod_resolved = Path(mod_file).resolve()
            except (ValueError, TypeError):
                continue

            try:
                if not mod_resolved.is_relative_to(source_path):
                    continue
            except (ValueError, TypeError):
                continue

            # This module is part of the target library and lives under the
            # source path -- instrument all its code objects.
            codes = _collect_code_objects(mod, source_path)
            for co in codes:
                instrument_code(co, events)

    def add_source(self, source: str | Path, library_name: str = ""):
        if isinstance(source, str):
            source = Path(source)
        if source.name.endswith("__init__.py"):
            source = source.parent
        resolved = source.resolve()
        print(f"DCOV: Adding {resolved} to sources")
        self.mpf.sources.append(resolved)

        # If library_name is known, try to instrument already-loaded sub-modules.
        # This covers the case where the library was imported before __enter__.
        # Fall back to the default library name set at init time.
        if not library_name:
            library_name = self.default_library_name or ""

        if library_name:
            self._instrument_already_loaded(resolved, library_name)

    def add_library(self, library_name: str):
        spec = find_spec(library_name)
        if spec is None or spec.origin is None:
            raise ImportError(f"Cannot find library {library_name}")
        self.add_source(spec.origin, library_name=library_name)
