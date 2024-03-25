results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-4, 8192, [3, 5])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
arg_1_tensor = np.random.uniform(-8, 128, [3, 4])
arg_1_tensor = oneflow.Tensor(arg_1_tensor)
arg_1 = oneflow.cast(arg_1_tensor,oneflow.float32)
arg_2_tensor = np.random.uniform(-32, 1024, [4, 5])
arg_2_tensor = oneflow.Tensor(arg_2_tensor)
arg_2 = oneflow.cast(arg_2_tensor,oneflow.float32)
results["res"] = oneflow.addmm(arg_0,arg_1,arg_2,)
