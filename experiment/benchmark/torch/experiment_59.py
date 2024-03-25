results = dict()
import torch

arg_0_tensor = torch.rand([2, 3], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1_tensor = torch.rand([2, 3], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([3, 3], dtype=torch.float32)
arg_2 = arg_2_tensor.clone()
results["res"] = torch.addmm(arg_0,arg_1,arg_2,)
