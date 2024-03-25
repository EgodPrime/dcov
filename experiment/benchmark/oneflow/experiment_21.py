results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0 = 4
arg_1 = 8
arg_2 = 2
batch_first = True
arg_class = oneflow.nn.LSTM(arg_0,arg_1,arg_2,batch_first=batch_first,)
arg_input_0_tensor = np.random.uniform(-1024, 4096, [2, 3, 4])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
