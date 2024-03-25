results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
kernel_size = 3
stride = 2
padding = 1
arg_class = oneflow.nn.AvgPool2d(kernel_size=kernel_size,stride=stride,padding=padding,)
arg_input_0_tensor = np.random.uniform(-32, 1024, [1, 3, 10, 20])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
