results = dict()
import torch

arg_0_tensor = torch.randint(-8192,128,[3, 3], dtype=torch.int64)
arg_0 = arg_0_tensor.clone()
arg_1_0 = 1
arg_1_1 = 2
arg_1_2 = 1
arg_1_3 = 0
arg_1 = [arg_1_0,arg_1_1,arg_1_2,arg_1_3,]
mode = "constant"
value = 0
results["res"] = torch.nn.functional.pad(arg_0,arg_1,mode=mode,value=value,)
