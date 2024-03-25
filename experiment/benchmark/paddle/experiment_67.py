results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 2],min = -256,max = 1024)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = 1.0507009873554805
arg_2 = 1.6732632423543772
arg_3 = None
results["res"] = paddle.nn.functional.selu(arg_0,arg_1,arg_2,arg_3,)
