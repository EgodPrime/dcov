results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_class = oneflow.nn.L1Loss()
arg_input_0_tensor = np.random.uniform(-32, 1024, [2, 4])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input_1_tensor = np.random.uniform(-8, 2, [2, 4])
arg_input_1_tensor = oneflow.Tensor(arg_input_1_tensor)
arg_input_1 = oneflow.cast(arg_input_1_tensor,oneflow.float32)
arg_input = [arg_input_0,arg_input_1,]
results["res"] = arg_class(*arg_input)
