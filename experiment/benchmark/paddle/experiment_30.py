results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [1, 2, 3, 4],min = -16,max = 64)
arg_0 = paddle.cast(arg_0_tensor,paddle.float64)
arg_1_tensor = paddle.uniform(shape = [1],min = -4,max = 2)
arg_1 = paddle.cast(arg_1_tensor,paddle.float64)
data_format = "NCHW"
results["res"] = paddle.nn.functional.prelu(arg_0,arg_1,data_format=data_format,)
