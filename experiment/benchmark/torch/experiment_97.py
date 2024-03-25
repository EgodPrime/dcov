results = dict()
import torch

arg_0_tensor = torch.rand([20, 16, 50], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1_tensor = torch.rand([33, 16, 3], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([33], dtype=torch.float32)
arg_2 = arg_2_tensor.clone()
arg_3_0 = 2
arg_3 = [arg_3_0,]
arg_4_0 = 0
arg_4 = [arg_4_0,]
arg_5_0 = 1
arg_5 = [arg_5_0,]
arg_6 = 1
results["res"] = torch.nn.functional.conv1d(arg_0,arg_1,arg_2,arg_3,arg_4,arg_5,arg_6,)
