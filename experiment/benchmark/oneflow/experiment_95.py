results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = oneflow.randint(-4, 16, [2, 3])
arg_0 = oneflow.cast(arg_0_tensor,oneflow.int64)
dim = 1
results["res"] = oneflow.cumprod(arg_0,dim=dim,)
