results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-4, 512, [1, 3, 4, 4])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
kernel_size = 3
stride = 1
padding = 1
results["res"] = oneflow.nn.functional.avg_pool2d(arg_0,kernel_size=kernel_size,stride=stride,padding=padding,)
