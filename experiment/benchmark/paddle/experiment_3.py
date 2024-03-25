results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [3, 3],min = -32,max = 1024)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
results["res"] = paddle.nonzero(arg_0,)
