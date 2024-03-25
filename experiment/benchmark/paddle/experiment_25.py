results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [2, 3, 8, 32, 32],min = -32768,max = 4)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
output_size = 3
data_format = "NCDHW"
name = None
results["res"] = paddle.nn.functional.adaptive_avg_pool3d(arg_0,output_size=output_size,data_format=data_format,name=name,)
