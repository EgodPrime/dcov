results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
kernel_size_0 = 3
kernel_size_1 = 3
kernel_size_2 = 3
kernel_size = [kernel_size_0,kernel_size_1,kernel_size_2,]
stride_0 = 2
stride_1 = 2
stride_2 = 2
stride = [stride_0,stride_1,stride_2,]
padding_0 = 1
padding_1 = 1
padding_2 = 1
padding = [padding_0,padding_1,padding_2,]
arg_class = oneflow.nn.AvgPool3d(kernel_size=kernel_size,stride=stride,padding=padding,)
arg_input_0_tensor = np.random.uniform(-4096, 32, [1, 3, 10, 20, 30])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
