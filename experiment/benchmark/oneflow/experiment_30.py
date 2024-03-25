results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-256, 2048, [1, 3, 10])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
kernel_size = 3
stride = 1
padding = 1
results["res"] = oneflow.nn.functional.avg_pool1d(arg_0,kernel_size=kernel_size,stride=stride,padding=padding,)
