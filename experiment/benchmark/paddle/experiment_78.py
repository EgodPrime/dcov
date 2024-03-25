results = dict()
import paddle

paddle.device.set_device("cpu")
kernel_size = 2
stride = 2
padding = 0
arg_class = paddle.nn.MaxPool3D(kernel_size=kernel_size,stride=stride,padding=padding,)
arg_input_0_tensor = paddle.uniform(shape = [1, 2, 3, 32, 32],min = -64,max = 4096)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
