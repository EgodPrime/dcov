results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [3],min = -64,max = 64)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
results["res"] = paddle.acos(arg_0,)
