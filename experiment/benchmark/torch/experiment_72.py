results = dict()
import torch

arg_0 = 1
arg_1 = 6
arg_class = torch.nn.GroupNorm(arg_0,arg_1,)
arg_input_0_tensor = torch.rand([20, 6, 10, 10], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
