results = dict()
import paddle

paddle.device.set_device("cpu")
shape_0 = 2
shape_1 = 3
shape = [shape_0,shape_1,]
dtype = "float32"
results["res"] = paddle.empty(shape=shape,dtype=dtype,)
