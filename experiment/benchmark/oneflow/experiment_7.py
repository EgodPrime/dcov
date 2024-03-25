results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-1024, 2, [1, 3, 4, 4])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
min_val = -1.0
max_val = 1.0
results["res"] = oneflow.nn.functional.hardtanh(arg_0,min_val=min_val,max_val=max_val,)
