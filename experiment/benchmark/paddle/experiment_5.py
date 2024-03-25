results = dict()
import paddle

paddle.device.set_device("cpu")
arg_class = paddle.nn.MSELoss()
arg_input_0_tensor = paddle.uniform(shape = [1],min = -32768,max = 512)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input_1_tensor = paddle.uniform(shape = [1],min = -2048,max = 128)
arg_input_1 = paddle.cast(arg_input_1_tensor,paddle.float32)
arg_input = [arg_input_0,arg_input_1,]
results["res"] = arg_class(*arg_input)
