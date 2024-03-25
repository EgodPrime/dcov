results = dict()
import torch

arg_0 = 3
stride = 2
arg_class = torch.nn.MaxUnpool3d(arg_0,stride=stride,)
arg_input_0_tensor = torch.rand([20, 16, 25, 16, 7], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input_1_tensor = torch.randint(3,4096,[20, 16, 25, 16, 7], dtype=torch.int64)
arg_input_1 = arg_input_1_tensor.clone()
arg_input = [arg_input_0,arg_input_1,]
results["res"] = arg_class(*arg_input)
