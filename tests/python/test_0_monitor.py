import sys

import pytest

from dcov import BitmapManager
from dcov.python.dcov_monitor import event_map, register_by_cov_type


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
            sys.monitoring.set_local_events(sys.monitoring.COVERAGE_ID, f.__code__, event)
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
            sys.monitoring.set_local_events(sys.monitoring.COVERAGE_ID, f.__code__, event)
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
            sys.monitoring.set_local_events(sys.monitoring.COVERAGE_ID, f.__code__, event)
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
            sys.monitoring.set_local_events(sys.monitoring.COVERAGE_ID, f.__code__, event)
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
            sys.monitoring.set_local_events(sys.monitoring.COVERAGE_ID, f.__code__, event)
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
