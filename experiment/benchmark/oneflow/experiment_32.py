results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_class = oneflow.nn.MSELoss()
arg_input_0_tensor = np.random.uniform(-32, 8192, [2, 4])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input_1_tensor = np.random.uniform(-16, 8192, [2, 4])
arg_input_1_tensor = oneflow.Tensor(arg_input_1_tensor)
arg_input_1 = oneflow.cast(arg_input_1_tensor,oneflow.float32)
arg_input = [arg_input_0,arg_input_1,]
results["res"] = arg_class(*arg_input)
