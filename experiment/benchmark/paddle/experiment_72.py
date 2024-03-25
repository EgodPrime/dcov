results = dict()
import paddle

paddle.device.set_device("cpu")
padding_0 = 1
padding_1 = 0
padding_2 = 1
padding_3 = 2
padding = [padding_0,padding_1,padding_2,padding_3,]
arg_class = paddle.nn.ZeroPad2D(padding=padding,)
arg_input_0_tensor = paddle.uniform(shape = [1, 1, 2, 3],min = -1024,max = 16)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
