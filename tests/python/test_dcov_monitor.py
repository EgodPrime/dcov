import sys
import types

import pytest

from dcov import BitmapManager
from dcov.python.dcov_monitor import event_map, register_by_cov_type
from dcov.python import dcov_loader as loader
from dcov.python import dcov_monitor as monitor


def f1(x: int):
    if x > 0:
        return x + 1
    elif x == 0:
        return x
    else:
        return x - 1


def f2(x: int, y: int):
    return x + y


def f3(x: int, y: str):
    try:
        return int(y) + x
    except ValueError:
        return "Error: y is not a valid integer"


def f4():
    f1(1)
    f1(0)
    f1(2)
    f2(1, 2)
    f3(1, "2")
    f3(1, "a")


@pytest.fixture
def bm():
    _bm = BitmapManager(4399)
    yield _bm
    _bm.close_bitmap()


def test_line(bm):
    c1 = bm.count_bitmap()
    assert c1 == 0
    register_by_cov_type("line", bm.set_bit, bm.bitmap_size)
    events = event_map["line"]
    sys.monitoring.restart_events()
    [
        [
            sys.monitoring.set_local_events(
                sys.monitoring.COVERAGE_ID, f.__code__, event
            )
            for event in events
        ]
        for f in [f1, f2, f3, f4]
    ]
    f1(1)
    c2 = bm.count_bitmap()
    assert c2 > 0
    f4()
    c3 = bm.count_bitmap()
    assert c3 > c2


def test_branch(bm):
    c1 = bm.count_bitmap()
    assert c1 == 0
    register_by_cov_type("branch", bm.set_bit, bm.bitmap_size)
    events = event_map["branch"]
    sys.monitoring.restart_events()
    [
        [
            sys.monitoring.set_local_events(
                sys.monitoring.COVERAGE_ID, f.__code__, event
            )
            for event in events
        ]
        for f in [f1, f2, f3, f4]
    ]
    f1(1)
    c2 = bm.count_bitmap()
    assert c2 > 0
    f4()
    c3 = bm.count_bitmap()
    assert c3 > c2


def test_function(bm):
    c1 = bm.count_bitmap()
    assert c1 == 0
    register_by_cov_type("function", bm.set_bit, bm.bitmap_size)
    events = event_map["function"]
    sys.monitoring.restart_events()
    [
        [
            sys.monitoring.set_local_events(
                sys.monitoring.COVERAGE_ID, f.__code__, event
            )
            for event in events
        ]
        for f in [f1, f2, f3, f4]
    ]
    f1(1)
    c2 = bm.count_bitmap()
    assert c2 > 0
    f4()
    c3 = bm.count_bitmap()
    assert c3 > c2


def test_block(bm):
    c1 = bm.count_bitmap()
    assert c1 == 0
    register_by_cov_type("block", bm.set_bit, bm.bitmap_size)
    events = event_map["block"]
    sys.monitoring.restart_events()
    [
        [
            sys.monitoring.set_local_events(
                sys.monitoring.COVERAGE_ID, f.__code__, event
            )
            for event in events
        ]
        for f in [f1, f2, f3, f4]
    ]
    f1(1)
    c2 = bm.count_bitmap()
    assert c2 > 0
    f4()
    c3 = bm.count_bitmap()
    assert c3 > c2


def test_edge(bm):
    c1 = bm.count_bitmap()
    assert c1 == 0
    register_by_cov_type("edge", bm.set_bit, bm.bitmap_size)
    events = event_map["edge"]
    sys.monitoring.restart_events()
    [
        [
            sys.monitoring.set_local_events(
                sys.monitoring.COVERAGE_ID, f.__code__, event
            )
            for event in events
        ]
        for f in [f1, f2, f3, f4]
    ]
    f1(1)
    c2 = bm.count_bitmap()
    assert c2 > 0
    f4()
    c3 = bm.count_bitmap()
    assert c3 > c2


def test_instrument_code_recurses(monkeypatch):
    calls = []

    def fake_set_local_events(tool_id, code, event):
        calls.append((tool_id, code, event))

    monkeypatch.setattr(sys.monitoring, "set_local_events", fake_set_local_events)

    def outer():
        def inner():
            return 1

        return inner()

    loader.instrument_code(outer, [1, 2])
    assert len(calls) >= 1


def test_instrument_code_on_code_obj(monkeypatch):
    calls = []

    def fake_set_local_events(tool_id, code, event):
        calls.append((tool_id, code, event))

    monkeypatch.setattr(sys.monitoring, "set_local_events", fake_set_local_events)
    code = compile("def f():\n    return 1", "f.py", "exec")
    loader.instrument_code(code, [sys.monitoring.events.LINE])
    assert len(calls) >= 1


def test_monitor_strhash_and_parts():
    h = monitor.strhash("abc")
    assert isinstance(h, int)
    v = monitor._sha256_of_parts(b"a", b"b")
    assert isinstance(v, int)


def test_monitor_hashes_and_callbacks():
    # small bitmap
    monitor._bitmap_size = 64
    assert 0 <= monitor.hash_si("a", 1) < 64
    assert 0 <= monitor.hash_sii("a", 1, 2) < 64
    assert 0 <= monitor.hash_sis("a", 1, "b") < 64

    calls = []
    monitor._hit_func = lambda n: calls.append(n)

    class FakeCode:
        co_filename = "file.py"
        co_firstlineno = 10

    code = FakeCode()
    assert monitor.line_callback(code, 1) == sys.monitoring.DISABLE
    assert monitor.function_callback(code, 1) == sys.monitoring.DISABLE
    assert monitor.branch_callback(code, 1, 2) == sys.monitoring.DISABLE
    assert monitor.jump_callback(code, 1, 2) == sys.monitoring.DISABLE
    class SmallHashException:
        def __hash__(self):
            return 2

    assert (
        monitor.exception_handle_callback(code, 1, SmallHashException())
        == sys.monitoring.DISABLE
    )
    assert len(calls) >= 5


def test_dcovloader_get_create_get_exec_success(monkeypatch):
    class FakeLoader:
        def create_module(self, spec):
            return types.ModuleType(spec.name)

        def get_code(self, name):
            return compile("x=2", "f.py", "exec")

    mod = types.ModuleType("m")
    dl = loader.DcovLoader(FakeLoader(), "line")
    assert isinstance(dl.create_module(types.SimpleNamespace(name="m")), types.ModuleType)
    assert isinstance(dl.get_code("m"), type(compile("", "", "exec")))
    # stub set_local_events
    monkeypatch.setattr(sys.monitoring, "set_local_events", lambda *a, **k: None)
    dl.exec_module(mod)
    assert mod.__dict__["x"] == 2


def test_dcov_loader_exec_module_exception_branch(monkeypatch):
    class FakeLoader:
        def get_code(self, name):
            return compile("raise RuntimeError('boom')", "fakefile", "exec")

        def exec_module(self, module):
            module.__dict__["fallback"] = True

    mod = types.ModuleType("m")
    dl = loader.DcovLoader(FakeLoader(), "line")
    # instrument_code may call into sys.monitoring.set_local_events; stub it
    monkeypatch.setattr(sys.monitoring, "set_local_events", lambda *a, **k: None)
    dl.exec_module(mod)
    assert mod.__dict__.get("fallback") is True

