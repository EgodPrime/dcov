results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
num_features = 4
arg_class = oneflow.nn.InstanceNorm1d(num_features=num_features,)
arg_input_0_tensor = np.random.uniform(-1024, 4096, [2, 4, 6])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
