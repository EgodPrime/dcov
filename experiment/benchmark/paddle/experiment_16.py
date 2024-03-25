results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 3],min = -512,max = 4096)
arg_0 = paddle.cast(arg_0_tensor,paddle.float64)
arg_1_tensor = paddle.uniform(shape = [3],min = -8,max = 4096)
arg_1 = paddle.cast(arg_1_tensor,paddle.float64)
results["res"] = paddle.mv(arg_0,arg_1,)
