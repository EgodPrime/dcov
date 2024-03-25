results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-32, 256, [2, 2])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
arg_1_tensor = np.random.uniform(-128, 16, [2, 2])
arg_1_tensor = oneflow.Tensor(arg_1_tensor)
arg_1 = oneflow.cast(arg_1_tensor,oneflow.float32)
results["res"] = oneflow.floor_divide(arg_0,arg_1,)
