results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [3, 9, 5],min = -256,max = 8)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
chunks = 3
axis = 1
results["res"] = paddle.chunk(arg_0,chunks=chunks,axis=axis,)
