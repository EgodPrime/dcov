results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [4],min = -2048,max = 16)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = 1
arg_2 = 20
arg_3 = None
results["res"] = paddle.nn.functional.softplus(arg_0,arg_1,arg_2,arg_3,)
