results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = oneflow.randint(-8, 4, [2, 6])
arg_0 = oneflow.cast(arg_0_tensor,oneflow.int64)
chunks = 3
dim = 1
results["res"] = oneflow.chunk(arg_0,chunks=chunks,dim=dim,)
