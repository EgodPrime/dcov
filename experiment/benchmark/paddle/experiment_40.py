results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 3],min = -4096,max = 2)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
results["res"] = paddle.numel(arg_0,)
