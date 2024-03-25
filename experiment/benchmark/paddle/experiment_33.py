results = dict()
import paddle

paddle.device.set_device("cpu")
arg_0_tensor = paddle.uniform(shape = [1, 1, 4, 4, 6],min = -64,max = 8)
arg_0 = paddle.cast(arg_0_tensor,paddle.float32)
kernel_size = 2
stride = 2
padding = 0
return_mask = True
results["res"] = paddle.nn.functional.max_pool3d(arg_0,kernel_size=kernel_size,stride=stride,padding=padding,return_mask=return_mask,)
