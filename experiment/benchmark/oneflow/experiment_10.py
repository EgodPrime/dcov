results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-4096, 64, [1, 3, 10])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
arg_1_tensor = np.random.uniform(-16, 4096, [4, 3, 3])
arg_1_tensor = oneflow.Tensor(arg_1_tensor)
arg_1 = oneflow.cast(arg_1_tensor,oneflow.float32)
stride = 1
padding = 1
results["res"] = oneflow.nn.functional.conv1d(arg_0,arg_1,stride=stride,padding=padding,)
