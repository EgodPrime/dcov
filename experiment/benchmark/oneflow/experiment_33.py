results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
kernel_size = 2
stride = 2
arg_class = oneflow.nn.MaxPool3d(kernel_size=kernel_size,stride=stride,)
arg_input_0_tensor = np.random.uniform(-256, 64, [2, 3, 6, 8, 8])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
