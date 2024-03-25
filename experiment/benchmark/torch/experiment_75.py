results = dict()
import torch

arg_0_tensor = torch.rand([1, 2, 3, 4, 5], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.numel(arg_0,)
