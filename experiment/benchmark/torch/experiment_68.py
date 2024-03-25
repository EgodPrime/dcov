results = dict()
import torch

margin = 1.0
p = 2
arg_class = torch.nn.TripletMarginLoss(margin=margin,p=p,)
arg_input_0_tensor = torch.rand([100, 128], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input_1_tensor = torch.rand([100, 128], dtype=torch.float32)
arg_input_1 = arg_input_1_tensor.clone()
arg_input_2_tensor = torch.rand([100, 128], dtype=torch.float32)
arg_input_2 = arg_input_2_tensor.clone()
arg_input = [arg_input_0,arg_input_1,arg_input_2,]
results["res"] = arg_class(*arg_input)
