import os
import subprocess

import dcov

a = r"""
import os
print(f"DCOV_KEY_PYTHON={os.environ.get('DCOV_KEY_PYTHON')}")
import importlib.util
from dcov.python.dcov_loader import LoaderWrapper
import dcov
spec = importlib.util.find_spec('torch')
assert spec, "Torch not installed"
with LoaderWrapper('line') as lw:
    lw.add_source(spec.origin)
    import torch
print(f"final coverage: {dcov.count_bits_py()}")
"""

b = r"""
import os
print(f"DCOV_KEY_PYTHON={os.environ.get('DCOV_KEY_PYTHON')}")
import importlib.util
import dcov
from dcov.python.dcov_loader import LoaderWrapper
spec = importlib.util.find_spec('torch')
assert spec, "Torch not installed"
with LoaderWrapper('line') as lw:
    lw.add_source(spec.origin)
    import torch
    a = torch.Tensor([-2])
    b = torch.Tensor([2])
    c = a + b
    # conv2d
    d = torch.nn.Conv2d(1, 1, 1)
print(f"final coverage: {dcov.count_bits_py()}")
"""


def f1():
    exec(a)


def f2():
    exec(b)


def test_torch_line():
    dcov.open_bitmap_x(43999)
    dcov.clear_bitmap_x(43999)
    dcov.open_bitmap_x(44009)
    dcov.clear_bitmap_x(44009)

    env = os.environ.copy()

    with open("/tmp/xx.py", "w") as f:
        f.write(a)
    env.update({"DCOV_KEY_PYTHON": "43999"})
    subprocess.run(["python", "/tmp/xx.py"], env=env)

    with open("/tmp/xx.py", "w") as f:
        f.write(b)
    env.update({"DCOV_KEY_PYTHON": "44009"})
    subprocess.run(["python", "/tmp/xx.py"], env=env)

    # delte the file
    os.remove("/tmp/xx.py")

    c1 = dcov.count_bits_x(43999)

    c2 = dcov.count_bits_x(44009)

    dcov.close_bitmap_x(43999)
    dcov.close_bitmap_x(44009)

    assert c1 > 0
    assert c2 > 0
    assert c1 != c2
