results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [4],min = -32,max = 8192)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
results["res"] = paddle.expm1(arg_0,)
