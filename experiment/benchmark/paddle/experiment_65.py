results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [1, 3, 32],min = -8192,max = 2048)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = 2
arg_2 = 2
arg_3 = 0
arg_4 = True
arg_5 = True
arg_6 = None
results["res"] = paddle.nn.functional.max_pool1d(arg_0,arg_1,arg_2,arg_3,arg_4,arg_5,arg_6,)
