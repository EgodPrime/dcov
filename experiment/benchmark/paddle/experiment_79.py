results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 2],min = -2048,max = 256)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1_tensor = paddle.uniform(shape = [2, 2],min = -16384,max = 1024)
arg_1 = paddle.cast(arg_1_tensor,paddle.float32)
arg_2 = "mean"
name = None
results["res"] = paddle.nn.functional.l1_loss(arg_0,arg_1,arg_2,name=name,)
