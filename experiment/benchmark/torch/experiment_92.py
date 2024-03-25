results = dict()
import torch

arg_0 = 256
arg_1 = 256
bidirectional = True
batch_first = True
arg_class = torch.nn.LSTM(arg_0,arg_1,bidirectional=bidirectional,batch_first=batch_first,)
arg_input_0_tensor = torch.rand([1, 15, 256], dtype=torch.float32)
arg_input_0 = arg_input_0_tensor.clone()
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
