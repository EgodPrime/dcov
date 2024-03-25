results = dict()
import torch

arg_0_tensor = torch.randint(-32768,64,[2], dtype=torch.int64)
arg_0 = arg_0_tensor.clone()
arg_1_tensor = torch.randint(-128,32768,[2], dtype=torch.int64)
arg_1 = arg_1_tensor.clone()
results["res"] = torch.equal(arg_0,arg_1,)
