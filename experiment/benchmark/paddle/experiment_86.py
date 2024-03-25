results = dict()
import paddle

paddle.device.set_device("cpu")
num_channels = 6
num_groups = 6
arg_class = paddle.nn.GroupNorm(num_channels=num_channels,num_groups=num_groups,)
arg_input_0_tensor = paddle.uniform(shape = [2, 6, 2, 2],min = -512,max = 1)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
