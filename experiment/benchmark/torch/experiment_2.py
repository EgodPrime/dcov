results = dict()
import torch

arg_0_tensor = torch.rand([2, 5], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
dim = 1
results["res"] = torch.nn.functional.log_softmax(arg_0,dim=dim,)
