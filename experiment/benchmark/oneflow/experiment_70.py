results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
input_size = 4
hidden_size = 2
num_layers = 1
batch_first = True
arg_class = oneflow.nn.RNN(input_size=input_size,hidden_size=hidden_size,num_layers=num_layers,batch_first=batch_first,)
arg_input_0_tensor = np.random.uniform(-1024, 1024, [1, 3, 4])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
