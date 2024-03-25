results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-1, 32768, [1, 4, 4, 4])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
dim = 1
results["res"] = oneflow.nn.functional.glu(arg_0,dim=dim,)
