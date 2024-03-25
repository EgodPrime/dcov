results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0 = 16
arg_1 = 32
arg_2 = 2
arg_class = paddle.nn.LSTM(arg_0,arg_1,arg_2,)
arg_input_0_tensor = paddle.uniform(shape = [4, 23, 16],min = -128,max = 4096)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input_1_0_tensor = paddle.uniform(shape = [2, 4, 32],min = -2048,max = 2048)
arg_input_1_0 = paddle.cast(arg_input_1_0_tensor,paddle.float32)
arg_input_1_1_tensor = paddle.uniform(shape = [2, 4, 32],min = -256,max = 512)
arg_input_1_1 = paddle.cast(arg_input_1_1_tensor,paddle.float32)
arg_input_1 = [arg_input_1_0,arg_input_1_1,]
arg_input = [arg_input_0,arg_input_1,]
results["res"] = arg_class(*arg_input)
