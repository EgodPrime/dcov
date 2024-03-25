results = dict()
import torch

arg_0_tensor = torch.randint(-64,16384,[2, 2, 2], dtype=torch.int64)
arg_0 = arg_0_tensor.clone()
arg_1_0 = 0
arg_1_1 = 1
arg_1 = [arg_1_0,arg_1_1,]
results["res"] = torch.flip(arg_0,arg_1,)
