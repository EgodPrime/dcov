results = dict()
import torch

arg_0_tensor = torch.rand([5], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
min_val = -1.0
max_val = 1.0
results["res"] = torch.nn.functional.hardtanh(arg_0,min_val=min_val,max_val=max_val,)
