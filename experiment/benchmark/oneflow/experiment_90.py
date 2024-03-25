results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
dim = 1
arg_class = oneflow.nn.LogSoftmax(dim=dim,)
arg_input_0_tensor = np.random.uniform(-4, 8, [2, 4])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
