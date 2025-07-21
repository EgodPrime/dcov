import importlib
import importlib.util
import os

import dcov
from dcov import LoaderWrapper


def test_torch_line():
    spec = importlib.util.find_spec("torch")
    assert spec is not None, "torch module not found"
    source = spec.origin
    assert source is not None, "torch module source not found"
    source = os.path.dirname(source)
    print(f"torch source is {source}")
    dcov.open_bitmap_py()
    dcov.clear_bitmap_py()
    with LoaderWrapper("line") as lw:
        lw.add_source(source)
        target = importlib.import_module("torch")
        print(target.__version__)
        a = target.abs(target.Tensor([-2]))
        assert a == 2, "abs function not working as expected"

    cov = dcov.count_bits_py()
    dcov.clear_bitmap_py()
    assert cov > 0
