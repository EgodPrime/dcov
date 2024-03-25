results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
num_groups = 2
num_channels = 4
arg_class = oneflow.nn.GroupNorm(num_groups=num_groups,num_channels=num_channels,)
arg_input_0_tensor = np.random.uniform(-16384, 2048, [2, 4, 6, 8])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
