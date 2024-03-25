results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 3, 8, 8],min = -32768,max = 1024)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1_tensor = paddle.uniform(shape = [6, 3, 3, 3],min = -256,max = 1)
arg_1 = paddle.cast(arg_1_tensor,paddle.float32)
results["res"] = paddle.nn.functional.conv2d(arg_0,arg_1,)
