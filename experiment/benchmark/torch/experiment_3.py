results = dict()
import torch

arg_0_tensor = torch.randint(-512,1,[2, 2, 2], dtype=torch.int64)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.flatten(arg_0,)
