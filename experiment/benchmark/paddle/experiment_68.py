results = dict()
import paddle

paddle.device.set_device("cpu")
arg_class = paddle.nn.Identity()
arg_input_0_tensor = paddle.uniform(shape = [3, 2],min = -512,max = 128)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
