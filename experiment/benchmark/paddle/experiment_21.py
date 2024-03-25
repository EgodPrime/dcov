results = dict()
import paddle

paddle.device.set_device("cpu")
arg_class = paddle.nn.LogSoftmax()
arg_input_0_tensor = paddle.uniform(shape = [2, 3, 4],min = -16384,max = 64)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
