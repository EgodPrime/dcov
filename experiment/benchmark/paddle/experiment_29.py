results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [1, 3, 32, 32],min = -32768,max = 32768)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
kernel_size = 2
stride = 2
padding = 0
ceil_mode = True
exclusive = True
divisor_override = None
data_format = "NCHW"
name = None
results["res"] = paddle.nn.functional.avg_pool2d(arg_0,kernel_size=kernel_size,stride=stride,padding=padding,ceil_mode=ceil_mode,exclusive=exclusive,divisor_override=divisor_override,data_format=data_format,name=name,)
