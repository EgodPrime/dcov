results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-8192, 8, [2, 3, 4, 4])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
p = 2
dim = 1
results["res"] = oneflow.nn.functional.normalize(arg_0,p=p,dim=dim,)
