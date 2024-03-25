results = dict()
import torch

arg_0_tensor = torch.rand([1, 64, 8, 9, 10], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1_0 = 5
arg_1_1 = 7
arg_1_2 = 9
arg_1 = [arg_1_0,arg_1_1,arg_1_2,]
results["res"] = torch.nn.functional.adaptive_avg_pool3d(arg_0,arg_1,)
