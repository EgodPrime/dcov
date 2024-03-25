results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [3],min = -8,max = 256)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = -1.0
arg_2 = 1.0
arg_3 = None
results["res"] = paddle.nn.functional.hardtanh(arg_0,arg_1,arg_2,arg_3,)
