results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [3],min = -1,max = 2)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
results["res"] = paddle.erfinv(arg_0,)
