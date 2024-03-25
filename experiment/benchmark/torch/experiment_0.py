results = dict()
import torch

arg_0_tensor = torch.rand([1, 1, 7], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1_0 = 3
arg_1 = [arg_1_0,]
arg_2_0 = 2
arg_2 = [arg_2_0,]
arg_3_0 = 0
arg_3 = [arg_3_0,]
arg_4 = False
arg_5 = True
results["res"] = torch.nn.functional.avg_pool1d(arg_0,arg_1,arg_2,arg_3,arg_4,arg_5,)
