results = dict()
import torch

arg_0 = 10
arg_1 = 20
arg_2 = 2
arg_class = torch.nn.RNN(arg_0,arg_1,arg_2,)
arg_input_0_tensor = torch.rand([5, 3, 10], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input_1_tensor = torch.rand([2, 3, 20], dtype=torch.float32)
arg_input_1 = arg_input_1_tensor.clone()
arg_input = [arg_input_0,arg_input_1,]
results["res"] = arg_class(*arg_input)
