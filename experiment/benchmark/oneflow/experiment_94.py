results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = oneflow.randint(-512, 8192, [3, 3])
arg_0 = oneflow.cast(arg_0_tensor,oneflow.int64)
results["res"] = oneflow.nonzero(arg_0,)
