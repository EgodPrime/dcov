results = dict()
import torch

arg_0_tensor = torch.rand([4, 4], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
dim = 1
results["res"] = torch.argsort(arg_0,dim=dim,)
