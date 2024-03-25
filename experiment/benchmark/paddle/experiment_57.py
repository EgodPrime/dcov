results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [3],min = -8192,max = 32768)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = None
results["res"] = paddle.nn.functional.relu6(arg_0,arg_1,)
