results = dict()
import torch

arg_0 = 5
arg_class = torch.nn.AdaptiveAvgPool1d(arg_0,)
arg_input_0_tensor = torch.rand([1, 64, 8], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
