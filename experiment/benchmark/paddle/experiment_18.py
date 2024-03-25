results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [1, 16, 5, 5],min = -2048,max = 1024)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = 1
results["res"] = paddle.flatten(arg_0,arg_1,)
