results = dict()
import paddle

paddle.device.set_device("cpu")
arg_class = paddle.nn.Hardswish()
arg_input_0_tensor = paddle.uniform(shape = [3],min = -8192,max = 16)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
