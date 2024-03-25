results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-512, 16, [1, 3, 8, 8, 8])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
kernel_size = 2
stride = 2
results["res"] = oneflow.nn.functional.max_pool3d(arg_0,kernel_size=kernel_size,stride=stride,)
