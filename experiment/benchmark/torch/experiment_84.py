results = dict()
import torch

scale_factor = 2
arg_class = torch.nn.UpsamplingNearest2d(scale_factor=scale_factor,)
arg_input_0_tensor = torch.rand([1, 1, 2, 2], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
