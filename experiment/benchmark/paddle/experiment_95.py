results = dict()
import paddle

paddle.device.set_device("cpu")
output_size = 16
arg_class = paddle.nn.AdaptiveAvgPool1D(output_size=output_size,)
arg_input_0_tensor = paddle.uniform(shape = [1, 3, 32],min = -4096,max = 32768)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input = [arg_input_0,]
results["res"] = arg_class(*arg_input)
