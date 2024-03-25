results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
alpha = 1.0
arg_class = oneflow.nn.ELU(alpha=alpha,)
arg_input_0_tensor = np.random.uniform(-1, 4, [2, 10])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
