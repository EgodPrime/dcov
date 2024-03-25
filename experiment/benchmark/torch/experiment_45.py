results = dict()
import torch

arg_0_tensor = torch.rand([12, 256, 8, 11], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
inplace = True
results["res"] = torch.nn.functional.relu6(arg_0,inplace=inplace,)
