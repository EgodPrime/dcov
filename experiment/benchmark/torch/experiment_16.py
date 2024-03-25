results = dict()
import torch

arg_0_tensor = torch.rand([16, 64, 36, 36], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
arg_1_tensor = torch.rand([1], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
results["res"] = torch.nn.functional.prelu(arg_0,arg_1,)
