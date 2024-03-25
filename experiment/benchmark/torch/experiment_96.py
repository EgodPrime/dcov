results = dict()
import torch

kernel_size = 3
stride = 2
padding = 1
arg_class = torch.nn.AvgPool2d(kernel_size=kernel_size,stride=stride,padding=padding,)
arg_input_0_tensor = torch.rand([1, 3, 10, 10], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
