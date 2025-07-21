library = "torch"
import importlib.util
from pathlib import Path

import dcov

spec = importlib.util.find_spec(library)
origin = spec.origin
print(f"source is {origin}")

with dcov.LoaderWrapper() as loader:
    loader.add_source(Path(origin).resolve())
    import torch

    torch.abs(torch.Tensor([-2]))
    print(f"final cov={dcov.count_bits_py()}")
