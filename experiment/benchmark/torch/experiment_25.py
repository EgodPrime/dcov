results = dict()
import torch

arg_0_tensor = torch.rand([2], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.expm1(arg_0,)
