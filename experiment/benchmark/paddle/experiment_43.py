results = dict()
import paddle

paddle.device.set_device("cpu")
arg_class = paddle.nn.L1Loss()
arg_input_0_tensor = paddle.uniform(shape = [2, 2],min = -64,max = 8192)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input_1_tensor = paddle.uniform(shape = [2, 2],min = -2048,max = 2048)
arg_input_1 = paddle.cast(arg_input_1_tensor,paddle.float32)
arg_input = [arg_input_0,arg_input_1,]
results["res"] = arg_class(*arg_input)
