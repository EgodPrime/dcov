results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
output_size_0 = 5
output_size_1 = 5
output_size = [output_size_0,output_size_1,]
arg_class = oneflow.nn.AdaptiveAvgPool2d(output_size=output_size,)
arg_input_0_tensor = np.random.uniform(-16384, 2048, [1, 3, 10, 20])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
