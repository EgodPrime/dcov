results = dict()
import torch

arg_class = torch.nn.L1Loss()
arg_input_0_tensor = torch.rand([3, 5], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input_1_tensor = torch.rand([3, 5], dtype=torch.float32)
arg_input_1 = arg_input_1_tensor.clone()
arg_input = [arg_input_0,arg_input_1,]
results["res"] = arg_class(*arg_input)
