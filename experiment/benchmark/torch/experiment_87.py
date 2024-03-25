results = dict()
import torch

arg_0_tensor = torch.rand([5, 1, 5], dtype=torch.float64)
arg_0 = arg_0_tensor.clone()
arg_1_tensor = torch.rand([5, 5], dtype=torch.float64)
arg_1 = arg_1_tensor.clone()
results["res"] = torch.atan2(arg_0,arg_1,)
