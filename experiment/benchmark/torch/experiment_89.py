results = dict()
import torch

arg_0 = 100
affine = True
arg_class = torch.nn.InstanceNorm3d(arg_0,affine=affine,)
arg_input_0_tensor = torch.rand([20, 100, 35, 45, 10], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
