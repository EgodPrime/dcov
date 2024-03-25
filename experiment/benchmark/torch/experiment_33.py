results = dict()
import torch

arg_0_tensor = torch.rand([20], dtype=torch.complex128)
arg_0 = arg_0_tensor.clone()
arg_1_tensor = torch.rand([20], dtype=torch.complex128)
arg_1 = arg_1_tensor.clone()
results["res"] = torch.dot(arg_0,arg_1,)
