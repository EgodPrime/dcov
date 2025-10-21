import os
import sys
from importlib import machinery
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import CodeType, FunctionType

from dcov.python.dcov_monitor import event_map, register_by_cov_type


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
            if isinstance(spec.loader, (machinery.ExtensionFileLoader, machinery.BuiltinImporter)):
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
    def __init__(self, cov_type="line"):
        self.class_name = cov_type
        register_by_cov_type(cov_type)
        self.mpf = DcovMetaPathFinder(cov_type)

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

    def add_source(self, source: str | Path):
        if isinstance(source, str):
            source = Path(source)
        if source.name.endswith("__init__.py"):
            source = source.parent
        print(f"DCOV: Adding {source} to sources")
        self.mpf.sources.append(source.resolve())
