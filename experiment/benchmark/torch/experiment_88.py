results = dict()
import torch

arg_0_tensor = torch.rand([20, 16, 50], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1 = 3
arg_2 = 2
arg_3 = 0
arg_4 = 1
arg_5 = False
arg_6 = False
results["res"] = torch.nn.functional.max_pool1d(arg_0,arg_1,arg_2,arg_3,arg_4,arg_5,arg_6,)
