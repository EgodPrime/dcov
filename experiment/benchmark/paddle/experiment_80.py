results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [4],min = -8192,max = 512)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
results["res"] = paddle.acosh(arg_0,)
