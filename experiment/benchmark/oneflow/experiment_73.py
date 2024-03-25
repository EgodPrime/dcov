results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-16384, 1, [1, 3, 10, 10, 10])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
output_size_0 = 5
output_size_1 = 5
output_size_2 = 5
output_size = [output_size_0,output_size_1,output_size_2,]
results["res"] = oneflow.nn.functional.adaptive_avg_pool3d(arg_0,output_size=output_size,)
