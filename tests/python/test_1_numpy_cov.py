import importlib
import importlib.util
import os

import dcov
from dcov import LoaderWrapper


def test_requests_line():
    spec = importlib.util.find_spec("numpy")
    assert spec is not None, "numpy module not found"
    source = spec.origin
    assert source is not None, "numpy module source not found"
    source = os.path.dirname(source)
    print(f"numpy source is {source}")
    dcov.open_bitmap_py()
    dcov.clear_bitmap_py()
    with LoaderWrapper("line") as lw:
        lw.add_source(source)
        target = importlib.import_module("numpy")
        print(target.__version__)
        a = target.abs(target.array([-2]))
        assert a == 2, "abs function not working as expected"

    cov = dcov.count_bitmap_py()
    dcov.clear_bitmap_py()
    assert cov > 0
