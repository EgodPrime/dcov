results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0 = 0.2
arg_class = paddle.nn.ELU(arg_0,)
arg_input_0_tensor = paddle.uniform(shape = [2, 2],min = -128,max = 1)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
