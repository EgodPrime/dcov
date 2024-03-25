results = dict()
import torch

arg_0_tensor = torch.rand([20, 16, 50, 44, 31], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1_0 = 3
arg_1_1 = 2
arg_1_2 = 2
arg_1 = [arg_1_0,arg_1_1,arg_1_2,]
arg_2_0 = 2
arg_2_1 = 1
arg_2_2 = 2
arg_2 = [arg_2_0,arg_2_1,arg_2_2,]
arg_3 = 0
arg_4 = 1
arg_5 = False
arg_6 = False
results["res"] = torch.nn.functional.max_pool3d(arg_0,arg_1,arg_2,arg_3,arg_4,arg_5,arg_6,)
