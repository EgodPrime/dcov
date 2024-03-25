results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 3, 4],min = -2048,max = 32768)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
arg_1 = -1
results["res"] = paddle.nn.functional.log_softmax(arg_0,arg_1,)
