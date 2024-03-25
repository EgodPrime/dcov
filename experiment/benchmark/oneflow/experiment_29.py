results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
padding_0 = 1
padding_1 = 2
padding_2 = 0
padding_3 = 1
padding = [padding_0,padding_1,padding_2,padding_3,]
arg_class = oneflow.nn.ZeroPad2d(padding=padding,)
arg_input_0_tensor = np.random.uniform(-256, 32768, [1, 1, 2, 2])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
