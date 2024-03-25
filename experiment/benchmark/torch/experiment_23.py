results = dict()
import torch

arg_0_tensor = torch.rand([3, 4], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.nn.functional.glu(arg_0,)
