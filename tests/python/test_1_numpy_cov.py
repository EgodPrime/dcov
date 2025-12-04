import importlib
import importlib.util
import os

from dcov import BitmapManager, LoaderWrapper


def test_requests_line():
    spec = importlib.util.find_spec("numpy")
    assert spec is not None, "numpy module not found"
    source = spec.origin
    assert source is not None, "numpy module source not found"
    source = os.path.dirname(source)
    print(f"numpy source is {source}")
    bm = BitmapManager(4399)
    with LoaderWrapper(bm, "line", "numpy") as lw:
        exec("import numpy; numpy.cov([[1, 2], [3, 4]])", {})

    cov = bm.count_bitmap()
    assert cov > 0
    bm.close_bitmap()
