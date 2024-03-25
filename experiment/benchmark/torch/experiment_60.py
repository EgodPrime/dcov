results = dict()
import torch

arg_0_tensor = torch.randint(-2048,128,[5], dtype=torch.int64)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.nonzero(arg_0,)
