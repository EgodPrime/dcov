results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [4],min = -32,max = 2)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1_tensor = paddle.uniform(shape = [4],min = -2,max = 256)
arg_1 = paddle.cast(arg_1_tensor,paddle.float32)
results["res"] = paddle.atan2(arg_0,arg_1,)
