results = dict()
import torch

arg_0_tensor = torch.rand([2, 3, 10, 10], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1_0 = 5
arg_1_1 = 5
arg_1 = [arg_1_0,arg_1_1,]
results["res"] = torch.nn.functional.adaptive_avg_pool2d(arg_0,arg_1,)
