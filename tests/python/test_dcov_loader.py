import types
import tempfile
from pathlib import Path

import pytest

from dcov.python.dcov_loader import (
    DcovLoader,
    DcovMetaPathFinder,
    LoaderWrapper,
    instrument_code,
)
from dcov import BitmapManager

def test_normal_use():
    bm = BitmapManager(4399)
    with LoaderWrapper(bm, "line", "numpy") as lw:
        exec("import numpy; numpy.cov([[1, 2], [3, 4]])", {})

    cov = bm.count_bitmap()
    assert cov > 0
    bm.close_bitmap()

class FakeMonitoring:
    def __init__(self):
        self.COVERAGE_ID = 42
        class E:
            LINE = 1
            BRANCH = 2
            PY_START = 3
            JUMP = 4

        self.events = E()
        self.DISABLE = object()
        self._tools = {}
        self.registered = []
        self.set_calls = []

    def get_tool(self, id):
        return self._tools.get(id)

    def use_tool_id(self, id, name):
        self._tools[id] = name

    def register_callback(self, id, event, callback):
        self.registered.append((id, event, callback))

    def set_local_events(self, id, code, event):
        self.set_calls.append((id, getattr(code, "co_firstlineno", None), event))


def test_instrument_code_function_and_nested(monkeypatch):
    fm = FakeMonitoring()
    monkeypatch.setattr(__import__("sys"), "monitoring", fm)

    def outer():
        x = 1

        def inner():
            return 2

        return inner

    instrument_code(outer, [fm.events.LINE])
    # outer and inner should have had events set
    assert len(fm.set_calls) >= 2


def test_dcov_loader_exec_module_success(monkeypatch):
    fm = FakeMonitoring()
    monkeypatch.setattr(__import__("sys"), "monitoring", fm)

    class FakeOrig:
        def get_code(self, name):
            return compile("a=1\ndef f():\n    return 2", "<test>", "exec")

    dl = DcovLoader(FakeOrig(), "line")
    module = types.ModuleType("m")
    module.__name__ = "m"
    dl.exec_module(module)
    assert module.a == 1
    assert module.f() == 2
    assert len(fm.set_calls) > 0


def test_dcov_loader_exec_module_exception_calls_orig_exec(monkeypatch):
    class FakeOrig:
        def get_code(self, name):
            raise RuntimeError("boom")

        def exec_module(self, module):
            module._ran = True

    dl = DcovLoader(FakeOrig(), "line")
    module = types.ModuleType("m")
    module.__name__ = "m"
    dl.exec_module(module)
    assert getattr(module, "_ran", False) is True


def test_mpf_find_spec_variants(monkeypatch, tmp_path):
    mpf = DcovMetaPathFinder("line")

    # First, an entry in meta_path without find_spec should be skipped
    class Dummy:
        pass

    class FakeFinder:
        def __init__(self, spec):
            self._spec = spec

        def find_spec(self, fullname, path, target=None):
            return self._spec

    # extension loader case
    class FakeExtLoader:
        pass

    spec_ext = types.SimpleNamespace(loader=FakeExtLoader(), origin="/tmp/mod.so")

    monkeypatch.setattr(__import__("sys"), "meta_path", [Dummy(), FakeFinder(spec_ext)])
    res = mpf.find_spec("something", None)
    assert res is spec_ext

    # suffix .so case
    spec_so = types.SimpleNamespace(loader=object(), origin=str(tmp_path / "lib.so"))
    monkeypatch.setattr(__import__("sys"), "meta_path", [FakeFinder(spec_so)])
    res = mpf.find_spec("something", None)
    assert res is spec_so

    # wrapping when source in sources
    file = tmp_path / "pkg" / "mod.py"
    file.parent.mkdir(parents=True)
    file.write_text("x=1")
    spec_py = types.SimpleNamespace(loader=object(), origin=str(file))
    monkeypatch.setattr(__import__("sys"), "meta_path", [FakeFinder(spec_py)])
    mpf.sources.append(tmp_path / "pkg")
    res = mpf.find_spec("pkg.mod", None)
    assert isinstance(res.loader, DcovLoader)


def test_loaderwrapper_behaviour(monkeypatch, tmp_path):
    fm = FakeMonitoring()
    monkeypatch.setattr(__import__("sys"), "monitoring", fm)

    bm = BitmapManager(64)

    # edge branch for hit_func
    lw = LoaderWrapper(bm, cov_type="edge")
    assert lw.class_name == "edge"

    # __enter__ and __exit__ removing from sys.meta_path even if not at index 0
    import sys

    # place mpf not at 0
    sys.meta_path = [object(), lw.mpf]
    lw.__exit__()
    assert lw.mpf not in sys.meta_path

    # add_source with __init__.py should use parent
    p = tmp_path / "pkg"
    p.mkdir()
    init = p / "__init__.py"
    init.write_text("")
    lw.add_source(str(init))
    assert any((p.resolve()) == s for s in lw.mpf.sources)

    # add_library failing raises
    with pytest.raises(ImportError):
        lw.add_library("nonexistent_package_abcdefg")

    # constructing with library_name that cannot be found raises
    with pytest.raises(ImportError):
        LoaderWrapper(bm, "line", "nonexistent_package_abcdefg")


def test_add_library_success(monkeypatch, tmp_path):
    origin = tmp_path / "lib.py"
    origin.write_text("")
    # patch find_spec used in the module
    import dcov.python.dcov_loader as loader_mod

    monkeypatch.setattr(loader_mod, "find_spec", lambda name: types.SimpleNamespace(origin=str(origin)))
    fm = FakeMonitoring()
    monkeypatch.setattr(__import__("sys"), "monitoring", fm)

    lw = LoaderWrapper(BitmapManager(32))
    lw.add_library("somepkg")
    assert any(Path(str(origin)).resolve() == s for s in lw.mpf.sources)


def test_instrument_already_loaded_module(monkeypatch, tmp_path):
    """Test that modules already in sys.modules get instrumented via add_source.

    This reproduces the real-world bug: yaml/requests are imported by
    openai/langchain before dcov's LoaderWrapper is created.
    """
    fm = FakeMonitoring()
    monkeypatch.setattr(__import__("sys"), "monitoring", fm)

    import sys

    # 1. Create a fake library on disk
    lib_dir = tmp_path / "mylib"
    lib_dir.mkdir()
    (lib_dir / "__init__.py").write_text("def hello():\n    return 42\n")
    (lib_dir / "sub.py").write_text("def sub_func():\n    x = 1\n    return x\n")

    # 2. Pre-import the library (simulates openai importing yaml before dcov)
    import importlib.util
    spec = importlib.util.spec_from_file_location("mylib", str(lib_dir / "__init__.py"))
    mod = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, "mylib", mod)
    spec.loader.exec_module(mod)

    sub_spec = importlib.util.spec_from_file_location(
        "mylib.sub", str(lib_dir / "sub.py")
    )
    sub_mod = importlib.util.module_from_spec(sub_spec)
    monkeypatch.setitem(sys.modules, "mylib.sub", sub_mod)
    sub_spec.loader.exec_module(sub_mod)

    # 3. Create LoaderWrapper and add the library (the new code path)
    from dcov.python.dcov_loader import LoaderWrapper
    from dcov import BitmapManager

    bm = BitmapManager(256)
    lw = LoaderWrapper(bm, cov_type="line")
    lw.add_source(str(lib_dir), library_name="mylib")

    # 4. Verify that code objects from already-loaded modules were instrumented
    #    (FakeMonitoring.set_calls records each set_local_events call)
    assert len(fm.set_calls) > 0, (
        "Expected already-loaded modules to be instrumented, but set_local_events was never called"
    )


def test_instrument_already_loaded_real_coverage(monkeypatch, tmp_path):
    """End-to-end: pre-import a module, then add it via add_library, verify coverage > 0."""
    import sys

    # 1. Create a fake library on disk with real code
    lib_dir = tmp_path / "covlib"
    lib_dir.mkdir()
    (lib_dir / "__init__.py").write_text(
        "def hello():\n    x = 1\n    y = 2\n    z = x + y\n    return z\n"
    )

    # 2. Pre-import before dcov
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "covlib", str(lib_dir / "__init__.py")
    )
    mod = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, "covlib", mod)
    spec.loader.exec_module(mod)

    # 3. NOW wrap with dcov
    from dcov.python.dcov_loader import LoaderWrapper
    from dcov import BitmapManager

    bm = BitmapManager(256)
    bm.clear_bitmap()

    with LoaderWrapper(bm, "line") as lw:
        lw.add_library("covlib")
        mod.hello()  # call the function

    cov = bm.count_bitmap()
    assert cov > 0, f"Expected coverage > 0 but got {cov}"
