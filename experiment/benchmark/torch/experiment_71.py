results = dict()
import torch

arg_0 = 3
stride = 2
arg_class = torch.nn.MaxPool1d(arg_0,stride=stride,)
arg_input_0_tensor = torch.rand([20, 16, 50], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
