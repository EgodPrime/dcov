results = dict()
import torch

arg_class = torch.nn.Identity()
arg_input_0_tensor = torch.rand([3, 1], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
