results = dict()
import torch

arg_0_0 = 3
arg_0_1 = 2
arg_0_2 = 2
arg_0 = [arg_0_0,arg_0_1,arg_0_2,]
stride_0 = 2
stride_1 = 1
stride_2 = 2
stride = [stride_0,stride_1,stride_2,]
arg_class = torch.nn.MaxPool3d(arg_0,stride=stride,)
arg_input_0_tensor = torch.rand([20, 16, 50, 44, 31], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
