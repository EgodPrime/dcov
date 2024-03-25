results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 2],min = -512,max = 32768)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = 0.2
arg_2 = None
results["res"] = paddle.nn.functional.celu(arg_0,arg_1,arg_2,)
