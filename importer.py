import sys
from importlib import machinery
from importlib.abc import Loader, MetaPathFinder
from pathlib import Path
from typing import Any

import bytecode as bc
from slipcover import VERSION, Slipcover


class SlipcoverLoader(Loader):
    def __init__(self, sci: Slipcover, orig_loader: Loader, origin: str):
        self.sci = sci  # Slipcover object measuring coverage
        self.orig_loader = orig_loader  # original loader we're wrapping
        self.origin = Path(origin)  # module origin (source file for a source loader)

        # loadlib checks for this attribute to see if we support it... keep in sync with orig_loader
        if not getattr(self.orig_loader, "get_resource_reader", None):
            delattr(self, "get_resource_reader")

    # for compability with loaders supporting resources, used e.g. by sklearn
    def get_resource_reader(self, fullname: str):
        return self.orig_loader.get_resource_reader(fullname)

    def create_module(self, spec):
        return self.orig_loader.create_module(spec)

    def get_code(self, name):  # expected by pyrun
        return self.orig_loader.get_code(name)

    def exec_module(self, module):
        code = self.orig_loader.get_code(module.__name__)

        self.sci.register_module(module)
        code = self.sci.instrument(code)
        exec(code, module.__dict__)


class FileMatcher:
    def __init__(self):
        self.cwd = Path.cwd()
        self.sources = []
        self.omit = []

        import inspect  # usually in Python lib

        # pip is usually in site-packages; importing it causes warnings

        self.pylib_paths = [Path(inspect.__file__).parent] + [
            Path(p) for p in sys.path if (Path(p) / "pip").exists()
        ]

    def addSource(self, source: Path):
        if isinstance(source, str):
            source = Path(source)
        if not source.is_absolute():
            source = self.cwd / source
        self.sources.append(source)

    def addOmit(self, omit):
        if not omit.startswith("*"):
            omit = self.cwd / omit

        self.omit.append(omit)

    def matches(self, filename: Path):
        if filename is None:
            return False

        if isinstance(filename, str):
            if filename == "built-in":
                return False  # can't instrument
            filename = Path(filename)

        if filename.suffix in (".pyd", ".so"):
            return False  # can't instrument DLLs

        if not filename.is_absolute():
            filename = self.cwd / filename

        if self.omit:
            from fnmatch import fnmatch

            if any(fnmatch(filename, o) for o in self.omit):
                return False

        if self.sources:
            return any(s in filename.parents for s in self.sources)

        if any(p in self.pylib_paths for p in filename.parents):
            return False

        return self.cwd in filename.parents


class MatchEverything:
    def __init__(self):
        pass

    def matches(self, filename: Path):
        return True


class SlipcoverMetaPathFinder(MetaPathFinder):
    def __init__(self, sci, file_matcher, debug=False):
        self.debug = debug
        self.sci = sci
        self.file_matcher = file_matcher

    def find_spec(self, fullname, path, target=None):
        if self.debug:
            print(f"Looking for {fullname}")

        for f in sys.meta_path:
            # skip ourselves
            if isinstance(f, SlipcoverMetaPathFinder):
                continue

            if not hasattr(f, "find_spec"):
                continue

            spec = f.find_spec(fullname, path, target)
            if spec is None or spec.loader is None:
                continue

            # can't instrument extension files
            if isinstance(spec.loader, machinery.ExtensionFileLoader):
                return None

            if self.file_matcher.matches(spec.origin):
                if self.debug:
                    print(f"instrumenting {fullname} from {spec.origin}")
                spec.loader = SlipcoverLoader(self.sci, spec.loader, spec.origin)

            return spec

        return None


class ImportManager:
    """A context manager that enables instrumentation while active."""

    def __init__(
        self, sci: Slipcover, file_matcher: FileMatcher = None, debug: bool = False
    ):
        self.mpf = SlipcoverMetaPathFinder(
            sci, file_matcher if file_matcher else MatchEverything(), debug
        )

    def __enter__(self) -> "ImportManager":
        sys.meta_path.insert(0, self.mpf)
        return self

    def __exit__(self, *args: Any) -> None:
        i = 0
        while i < len(sys.meta_path):
            if sys.meta_path[i] is self.mpf:
                sys.meta_path.pop(i)
                break
            i += 1
