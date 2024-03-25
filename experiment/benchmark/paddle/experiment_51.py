results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0 = 4
arg_1 = 6
arg_2_0 = 3
arg_2_1 = 3
arg_2_2 = 3
arg_2 = [arg_2_0,arg_2_1,arg_2_2,]
arg_class = paddle.nn.Conv3D(arg_0,arg_1,arg_2,)
arg_input_0_tensor = paddle.uniform(shape = [2, 4, 8, 8, 8],min = -2048,max = 32)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
