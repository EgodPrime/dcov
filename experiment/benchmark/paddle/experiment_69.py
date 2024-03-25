results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [4],min = -1,max = 64)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = None
results["res"] = paddle.nn.functional.tanh(arg_0,arg_1,)
