results = dict()
import torch

inplace = True
arg_class = torch.nn.ELU(inplace=inplace,)
arg_input_0_tensor = torch.rand([16, 3, 256], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
