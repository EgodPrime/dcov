results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [4],min = -16,max = 4)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = None
results["res"] = paddle.nn.functional.softsign(arg_0,arg_1,)
