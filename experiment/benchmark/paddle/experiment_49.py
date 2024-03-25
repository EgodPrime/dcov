results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [3, 1, 7, 112, 112],min = -32768,max = 8192)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
kernel_size_0 = 5
kernel_size_1 = 1
kernel_size_2 = 1
kernel_size = [kernel_size_0,kernel_size_1,kernel_size_2,]
stride = 1
results["res"] = paddle.nn.functional.avg_pool3d(arg_0,kernel_size=kernel_size,stride=stride,)
