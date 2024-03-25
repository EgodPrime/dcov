results = dict()
import paddle

paddle.device.set_device("cpu")
start_axis = 1
stop_axis = 2
arg_class = paddle.nn.Flatten(start_axis=start_axis,stop_axis=stop_axis,)
arg_input_0_tensor = paddle.uniform(shape = [5, 2, 3, 4],min = -4,max = 256)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
