results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 3, 32, 32],min = -32,max = 1024)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
output_size = 3
data_format = "NCHW"
name = None
results["res"] = paddle.nn.functional.adaptive_avg_pool2d(arg_0,output_size=output_size,data_format=data_format,name=name,)
