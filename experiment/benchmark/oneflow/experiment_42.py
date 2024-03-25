results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
in_channels = 3
out_channels = 16
kernel_size = 3
stride = 1
padding = 1
bias = True
arg_class = oneflow.nn.Conv3d(in_channels=in_channels,out_channels=out_channels,kernel_size=kernel_size,stride=stride,padding=padding,bias=bias,)
arg_input_0_tensor = np.random.uniform(-4096, 2048, [2, 3, 16, 32, 32])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
