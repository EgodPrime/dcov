results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_tensor = np.random.uniform(-2048, 32768, [1, 3, 10, 10])
arg_0_tensor = oneflow.Tensor(arg_0_tensor)
arg_0 = oneflow.cast(arg_0_tensor,oneflow.float32)
output_size_0 = 5
output_size_1 = 5
output_size = [output_size_0,output_size_1,]
results["res"] = oneflow.nn.functional.adaptive_avg_pool2d(arg_0,output_size=output_size,)
