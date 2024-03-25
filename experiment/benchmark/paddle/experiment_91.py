results = dict()
import paddle

paddle.device.set_device("cpu")
x_tensor = paddle.uniform(shape = [2, 3, 4],min = -16384,max = 128)
x = paddle.cast(x_tensor,paddle.float32)
axis = -1
results["res"] = paddle.sort(x=x,axis=axis,)
