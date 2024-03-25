results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-1, 32768, [1, 3, 10, 10])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
arg_1_tensor = np.random.uniform(-8, 32, [4, 3, 3, 3])
arg_1_tensor = oneflow.Tensor(arg_1_tensor)
arg_1 = oneflow.cast(arg_1_tensor,oneflow.float32)
stride = 1
padding = 1
results["res"] = oneflow.nn.functional.conv2d(arg_0,arg_1,stride=stride,padding=padding,)
