results = dict()
import torch

arg_0 = 32
affine = True
arg_class = torch.nn.InstanceNorm2d(arg_0,affine=affine,)
arg_input_0_tensor = torch.rand([1, 32, 1080, 1080], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
