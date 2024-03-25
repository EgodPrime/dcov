results = dict()
import torch

arg_0_tensor = torch.rand([2], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1 = 1.0
arg_2 = False
results["res"] = torch.nn.functional.celu(arg_0,arg_1,arg_2,)
