results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [1],min = -32768,max = 128)
arg_0 = paddle.cast(arg_0_tensor,paddle.float64)
results["res"] = paddle.ceil(arg_0,)
