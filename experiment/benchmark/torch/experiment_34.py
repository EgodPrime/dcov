results = dict()
import torch

arg_0_tensor = torch.rand([2], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1 = False
results["res"] = torch.nn.functional.selu(arg_0,arg_1,)
