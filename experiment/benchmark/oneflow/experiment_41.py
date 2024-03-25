results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
scale_factor = 2
arg_class = oneflow.nn.UpsamplingBilinear2d(scale_factor=scale_factor,)
arg_input_0_tensor = np.random.uniform(-8192, 4, [2, 3, 4, 4])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
