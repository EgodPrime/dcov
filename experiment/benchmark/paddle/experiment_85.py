results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [3],min = -256,max = 4096)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
name = None
results["res"] = paddle.nn.functional.hardsigmoid(arg_0,name=name,)
