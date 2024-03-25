results = dict()
import torch

arg_0_tensor = torch.rand([16, 3, 144, 144], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
results["res"] = torch.nn.functional.tanh(arg_0,)
