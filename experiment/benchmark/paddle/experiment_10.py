results = dict()
import paddle

paddle.device.set_device("cpu")
p = 0.5
arg_class = paddle.nn.Dropout3D(p=p,)
arg_input_0_tensor = paddle.uniform(shape = [1, 2, 2, 2, 3],min = -128,max = 64)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
