results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.randint(shape = [3, 4],low = -8192,high = 128)
arg_0 = paddle.cast(arg_0_tensor,paddle.int64)
results["res"] = paddle.argmax(arg_0,)
