results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.randint(shape = [3, 4],low = -32,high = 256)
arg_0 = paddle.cast(arg_0_tensor,paddle.int64)
dim = 0
results["res"] = paddle.cumprod(arg_0,dim=dim,)
