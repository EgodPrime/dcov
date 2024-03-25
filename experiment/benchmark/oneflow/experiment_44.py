results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-8, 8192, [2, 3])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
dim = 1
results["res"] = oneflow.nn.functional.log_softmax(arg_0,dim=dim,)
