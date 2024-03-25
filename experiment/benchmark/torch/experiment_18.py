results = dict()
import torch

arg_0_tensor = torch.rand([1, 64, 8], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1 = 5
results["res"] = torch.nn.functional.adaptive_avg_pool1d(arg_0,arg_1,)
