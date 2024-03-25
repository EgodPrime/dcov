results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 3, 4],min = -8,max = 4096)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
axis = -1
results["res"] = paddle.argsort(arg_0,axis=axis,)
