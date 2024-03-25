results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0 = 3
arg_1 = 2
arg_2 = 3
arg_class = paddle.nn.Conv1D(arg_0,arg_1,arg_2,)
arg_input_0_tensor = paddle.uniform(shape = [1, 3, 4],min = -256,max = 16)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
