results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-4, 1, [2, 3, 4])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
pad_0 = 1
pad_1 = 1
pad_2 = 2
pad_3 = 2
pad_4 = 3
pad_5 = 3
pad = [pad_0,pad_1,pad_2,pad_3,pad_4,pad_5,]
mode = "constant"
value = 0
results["res"] = oneflow.nn.functional.pad(arg_0,pad=pad,mode=mode,value=value,)
