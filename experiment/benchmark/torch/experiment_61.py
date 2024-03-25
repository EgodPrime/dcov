results = dict()
import torch

arg_0_tensor = torch.rand([3, 3], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
dim = 0
results["res"] = torch.cumprod(arg_0,dim=dim,)
