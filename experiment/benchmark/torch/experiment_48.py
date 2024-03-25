results = dict()
import torch

arg_0_tensor = torch.rand([2, 3, 10, 10], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1_tensor = torch.rand([4, 3, 3, 3], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
stride = 1
padding = 1
results["res"] = torch.nn.functional.conv2d(arg_0,arg_1,stride=stride,padding=padding,)
