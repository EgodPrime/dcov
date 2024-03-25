results = dict()
import torch

dim = -1
arg_class = torch.nn.Softmax(dim=dim,)
arg_input_0_tensor = torch.rand([4, 12, 141, 141], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
