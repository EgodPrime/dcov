results = dict()
import torch

arg_0_tensor = torch.rand([2485, 32], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.exp(arg_0,)
