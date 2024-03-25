results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
margin = 1.0
p = 2
arg_class = oneflow.nn.TripletMarginLoss(margin=margin,p=p,)
arg_input_0_tensor = np.random.uniform(-8192, 64, [3, 128])
arg_input_0_tensor = oneflow.Tensor(arg_input_0_tensor)
arg_input_0 = oneflow.cast(arg_input_0_tensor,oneflow.float32)
arg_input_1_tensor = np.random.uniform(-256, 256, [3, 128])
arg_input_1_tensor = oneflow.Tensor(arg_input_1_tensor)
arg_input_1 = oneflow.cast(arg_input_1_tensor,oneflow.float32)
arg_input_2_tensor = np.random.uniform(-32768, 32768, [3, 128])
arg_input_2_tensor = oneflow.Tensor(arg_input_2_tensor)
arg_input_2 = oneflow.cast(arg_input_2_tensor,oneflow.float32)
arg_input = [arg_input_0,arg_input_1,arg_input_2,]
results["res"] = arg_class(*arg_input)
