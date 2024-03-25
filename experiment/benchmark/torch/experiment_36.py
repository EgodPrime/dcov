results = dict()
import torch

arg_0_tensor = torch.rand([5, 10, 5], dtype=torch.float64)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.sort(arg_0,)
