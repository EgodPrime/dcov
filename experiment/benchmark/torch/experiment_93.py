results = dict()
import torch

arg_0_tensor = torch.rand([8, 3], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1 = 8
arg_2 = 1
results["res"] = torch.chunk(arg_0,arg_1,arg_2,)
