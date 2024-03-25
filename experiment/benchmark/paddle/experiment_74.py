results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [1, 3, 32],min = -4096,max = 2)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = 16
arg_2 = None
results["res"] = paddle.nn.functional.adaptive_avg_pool1d(arg_0,arg_1,arg_2,)
