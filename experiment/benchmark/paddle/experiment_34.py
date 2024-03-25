results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.randint(shape = [1],low = -64,high = 4096)
arg_0 = paddle.cast(arg_0_tensor,paddle.int64)
arg_1 = 0
results["res"] = paddle.equal(arg_0,arg_1,)
