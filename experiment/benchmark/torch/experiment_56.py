results = dict()
import torch

arg_0_tensor = torch.rand([5, 512], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
dim = 1
results["res"] = torch.nn.functional.normalize(arg_0,dim=dim,)
