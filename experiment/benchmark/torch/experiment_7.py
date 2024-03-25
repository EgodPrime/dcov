results = dict()
import torch

arg_0_tensor = torch.rand([2], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
inplace = False
results["res"] = torch.nn.functional.silu(arg_0,inplace=inplace,)
