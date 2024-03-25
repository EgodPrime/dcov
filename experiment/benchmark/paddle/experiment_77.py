results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_0_tensor = paddle.uniform(shape = [2],min = -8,max = 512)
arg_0_0 = paddle.cast(arg_0_0_tensor,paddle.float64)
arg_0_1_tensor = paddle.uniform(shape = [2],min = -16,max = 1024)
arg_0_1 = paddle.cast(arg_0_1_tensor,paddle.float64)
arg_0 = [arg_0_0,arg_0_1,]
arg_1 = 0
results["res"] = paddle.stack(arg_0,arg_1,)
