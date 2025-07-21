import hashlib
import os
import sys
from types import CodeType

from dcov.python.dcov_py import get_bitmap_size, on_hit_py, on_hit_py_edge

bitmap_size = get_bitmap_size()

FNV_OFFSET_BASIS = 216613626
FNV_PRIME = 16777219


def strhash(s: str):
    ho = hashlib.sha256(s.encode("utf-8"))
    return int(ho.hexdigest(), 16)


def hash_si(s1: str, i1: int) -> int:
    h = FNV_OFFSET_BASIS ^ strhash(s1) * FNV_PRIME ^ i1
    return h % bitmap_size


def hash_sii(s1: str, i1: int, i2: int) -> int:
    h = FNV_OFFSET_BASIS ^ strhash(s1) * FNV_PRIME ^ i1 * FNV_PRIME ^ i2
    return h % bitmap_size


def hash_sis(s1: str, i1: int, s2: str) -> int:
    h = FNV_OFFSET_BASIS ^ strhash(s1) * FNV_PRIME ^ i1 * FNV_PRIME ^ strhash(s2)
    return h % bitmap_size


def line_callback(code: CodeType, line_number: int):
    # print(f"Line {code.co_filename}:{line_number} with {hash_si(code.co_filename, line_number)}")
    hit_func(hash_si(code.co_filename, line_number))
    return sys.monitoring.DISABLE


def function_callback(code: CodeType, instruction_offset: int):
    # print(f"Function {code.co_filename}:{code.co_firstlineno} with {hash_si(code.co_filename, code.co_firstlineno)}")
    hit_func(hash_si(code.co_filename, code.co_firstlineno))
    return sys.monitoring.DISABLE


def branch_callback(code: CodeType, instruction_offset: int, destination_offset: int):
    # print(f"Branch {code.co_filename}:{instruction_offset}->{destination_offset} with {hash_sii(code.co_filename, instruction_offset, destination_offset)}")
    hit_func(hash_sii(code.co_filename, instruction_offset, destination_offset))
    return sys.monitoring.DISABLE


def jump_callback(code: CodeType, instruction_offset: int, destination_offset: int):
    # print(f"Jump {code.co_filename}:{instruction_offset}->{destination_offset} with {hash_sii(code.co_filename, instruction_offset, destination_offset)}")
    hit_func(hash_sii(code.co_filename, instruction_offset, destination_offset))
    return sys.monitoring.DISABLE


def exception_handle_callback(code: CodeType, instruction_offset: int, exception: BaseException):
    # print(f"Exception {code.co_filename}:{instruction_offset} with {hash_si(code.co_filename, instruction_offset)}")
    hit_func(hash_sii(code.co_filename, instruction_offset, hash(exception)))
    return sys.monitoring.DISABLE


hit_func = None

"""
At Python3.13, BRANCH and JUMP are the same events. We found this according 
to the Document:
If another callback was registered for the given tool_id and event, it is unregistered and returned. Otherwise register_callback() returns None.

And EXCEPTION_HANDLED is not a valid event currently.... with error `invalid local event set 0x800`
"""

event_map = {
    "line": [sys.monitoring.events.LINE],
    "branch": [sys.monitoring.events.BRANCH],
    "function": [sys.monitoring.events.PY_START],
    "jump": [sys.monitoring.events.JUMP],
    "block": [
        sys.monitoring.events.BRANCH,
        sys.monitoring.events.PY_START,
        #    sys.monitoring.events.JUMP,
        #    sys.monitoring.events.EXCEPTION_HANDLED
    ],
    "edge": [
        sys.monitoring.events.BRANCH,
        sys.monitoring.events.PY_START,
        #  sys.monitoring.events.JUMP,
        #  sys.monitoring.events.EXCEPTION_HANDLED
    ],
}

callback_map = {
    "line": [line_callback],
    "branch": [branch_callback],
    "function": [function_callback],
    "jump": [jump_callback],
    "block": [
        branch_callback,
        function_callback,
        #   jump_callback,
        #   exception_handle_callback
    ],
    "edge": [
        branch_callback,
        function_callback,
        #  jump_callback,
        #  exception_handle_callback
    ],
}


def register_by_cov_type(cov_type: str):
    if sys.monitoring.get_tool(sys.monitoring.COVERAGE_ID) != "dcov":
        sys.monitoring.use_tool_id(sys.monitoring.COVERAGE_ID, "dcov")

    global hit_func
    if cov_type == "edge":
        hit_func = on_hit_py_edge
    else:
        hit_func = on_hit_py

    for event, callback in zip(event_map[cov_type], callback_map[cov_type]):
        print(f"register event {event} to {callback.__name__}")
        sys.monitoring.register_callback(sys.monitoring.COVERAGE_ID, event, callback)
