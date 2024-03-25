results = dict()
import torch

arg_0 = 16
arg_1 = 33
arg_2_0 = 3
arg_2_1 = 5
arg_2_2 = 2
arg_2 = [arg_2_0,arg_2_1,arg_2_2,]
stride_0 = 2
stride_1 = 1
stride_2 = 1
stride = [stride_0,stride_1,stride_2,]
padding_0 = 4
padding_1 = 2
padding_2 = 0
padding = [padding_0,padding_1,padding_2,]
arg_class = torch.nn.Conv3d(arg_0,arg_1,arg_2,stride=stride,padding=padding,)
arg_input_0_tensor = torch.rand([20, 16, 10, 50, 100], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
