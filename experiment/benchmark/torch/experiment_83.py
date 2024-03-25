results = dict()
import torch

arg_0_tensor = torch.rand([], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.ceil(arg_0,)
