import ctypes
from pathlib import Path

exp = ctypes.CDLL(Path(__file__).resolve().parent.joinpath("libexample.so"))

test_switch = exp.test_switch
test_switch.argtypes = [ctypes.c_int, ctypes.c_int]


def test_py(a: int, b: int):
    if a:
        if b == 1:
            test_switch(1, 1)
        elif b == 2:
            test_switch(1, 2)
        elif b == 3:
            test_switch(1, 3)
        else:
            test_switch(1, 4)
    else:
        if b == 1:
            test_switch(0, 1)
        elif b == 2:
            test_switch(0, 2)
        elif b == 3:
            test_switch(0, 3)
        else:
            test_switch(0, 4)
