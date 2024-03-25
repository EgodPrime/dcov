results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.randint(shape = [3, 2, 2],low = -32,high = 64)
arg_0 = paddle.cast(arg_0_tensor,paddle.int64)
arg_1_0 = 0
arg_1_1 = 1
arg_1 = [arg_1_0,arg_1_1,]
results["res"] = paddle.flip(arg_0,arg_1,)
