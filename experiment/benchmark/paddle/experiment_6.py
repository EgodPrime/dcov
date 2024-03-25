results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [1, 1, 2, 3],min = -4096,max = 1024)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
pad_0 = 1
pad_1 = 0
pad_2 = 1
pad_3 = 2
pad = [pad_0,pad_1,pad_2,pad_3,]
mode = "constant"
value = 0.0
data_format = "NCHW"
name = None
results["res"] = paddle.nn.functional.pad(arg_0,pad=pad,mode=mode,value=value,data_format=data_format,name=name,)
