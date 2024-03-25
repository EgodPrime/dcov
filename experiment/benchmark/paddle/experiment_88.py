results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 3],min = -16384,max = 4096)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
results["res"] = paddle.nn.functional.normalize(arg_0,)
