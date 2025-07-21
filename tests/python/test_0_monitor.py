import os
import sys

from dcov import clear_bitmap_py, close_bitmap_py, count_bits_py, open_bitmap_py
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


def test_line():
    open_bitmap_py()
    clear_bitmap_py()
    c1 = count_bits_py()
    assert c1 == 0
    register_by_cov_type("line")
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
    c2 = count_bits_py()
    assert c2 > 0
    f4()
    c3 = count_bits_py()
    assert c3 > c2
    close_bitmap_py()


def test_branch():
    open_bitmap_py()
    clear_bitmap_py()
    c1 = count_bits_py()
    assert c1 == 0
    register_by_cov_type("branch")
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
    c2 = count_bits_py()
    assert c2 > 0
    f4()
    c3 = count_bits_py()
    assert c3 > c2
    close_bitmap_py()


def test_function():
    open_bitmap_py()
    clear_bitmap_py()
    c1 = count_bits_py()
    assert c1 == 0
    register_by_cov_type("function")
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
    c2 = count_bits_py()
    assert c2 > 0
    f4()
    c3 = count_bits_py()
    assert c3 > c2
    close_bitmap_py()


def test_block():
    open_bitmap_py()
    clear_bitmap_py()
    c1 = count_bits_py()
    assert c1 == 0
    register_by_cov_type("block")
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
    c2 = count_bits_py()
    assert c2 > 0
    f4()
    c3 = count_bits_py()
    assert c3 > c2
    close_bitmap_py()


def test_edge():
    open_bitmap_py()
    clear_bitmap_py()
    c1 = count_bits_py()
    assert c1 == 0
    register_by_cov_type("edge")
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
    c2 = count_bits_py()
    assert c2 > 0
    f4()
    c3 = count_bits_py()
    assert c3 > c2
    close_bitmap_py()
