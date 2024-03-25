results = dict()
import torch

arg_0_0 = 5
arg_0_1 = 5
arg_0 = [arg_0_0,arg_0_1,]
arg_class = torch.nn.AdaptiveAvgPool2d(arg_0,)
arg_input_0_tensor = torch.rand([1, 3, 10, 10], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
