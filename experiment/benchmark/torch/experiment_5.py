results = dict()
import torch

arg_0_tensor = torch.rand([784, 1200], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
beta = 1
threshold = 20
results["res"] = torch.nn.functional.softplus(arg_0,beta=beta,threshold=threshold,)
