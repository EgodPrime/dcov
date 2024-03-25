results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
lambd = 0.5
arg_class = oneflow.nn.Softshrink(lambd=lambd,)
arg_input_0_tensor = np.random.uniform(-8, 2048, [2, 3, 4])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
