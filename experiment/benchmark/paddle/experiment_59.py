results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.randint(shape = [3],low = -8192,high = 4)
arg_0 = paddle.cast(arg_0_tensor,paddle.int64)
arg_1_tensor = paddle.randint(shape = [3],low = -256,high = 16384)
arg_1 = paddle.cast(arg_1_tensor,paddle.int64)
results["res"] = paddle.dot(arg_0,arg_1,)
