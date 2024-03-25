results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-32768, 8192, [2, 3])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
arg_1_0 = 1
arg_1 = [arg_1_0,]
results["res"] = oneflow.flip(arg_0,arg_1,)
