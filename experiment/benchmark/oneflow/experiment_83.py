results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
num_parameters = 1
init = 0.25
arg_class = oneflow.nn.PReLU(num_parameters=num_parameters,init=init,)
arg_input_0_tensor = np.random.uniform(-32768, 64, [2, 3])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
