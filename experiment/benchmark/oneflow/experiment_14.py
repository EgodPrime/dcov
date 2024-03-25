results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = oneflow.randint(-16, 8, [3])
arg_0 = oneflow.cast(arg_0_tensor,oneflow.int64)
results["res"] = oneflow.rsqrt(arg_0,)
