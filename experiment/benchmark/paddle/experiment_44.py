results = dict()
import paddle

paddle.device.set_device("cpu")
x_tensor = paddle.uniform(shape = [4],min = -8,max = 1024)
x = paddle.cast(x_tensor,paddle.float32)
results["res"] = paddle.sign(x=x,)
