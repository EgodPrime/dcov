results = dict()
import torch

arg_0_tensor = torch.rand([5, 512, 1, 1, 1], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.rsqrt(arg_0,)
