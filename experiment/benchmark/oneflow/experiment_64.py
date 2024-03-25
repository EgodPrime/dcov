results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-4, 2, [2, 3])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
results["res"] = oneflow.floor(arg_0,)
