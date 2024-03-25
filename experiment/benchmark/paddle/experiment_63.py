results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [1, 3, 4],min = -8192,max = 1)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1_tensor = paddle.uniform(shape = [2, 3, 3],min = -8,max = 512)
arg_1 = paddle.cast(arg_1_tensor,paddle.float32)
bias_tensor = paddle.uniform(shape = [2],min = -32768,max = 32768)
bias = paddle.cast(bias_tensor,paddle.float32)
padding = 0
stride_0 = 1
stride = [stride_0,]
dilation_0 = 1
dilation = [dilation_0,]
groups = 1
data_format = "NCL"
results["res"] = paddle.nn.functional.conv1d(arg_0,arg_1,bias=bias,padding=padding,stride=stride,dilation=dilation,groups=groups,data_format=data_format,)
