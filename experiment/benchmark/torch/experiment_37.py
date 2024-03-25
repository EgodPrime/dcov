results = dict()
import torch

arg_0_tensor = torch.rand([2, 3, 10, 10], dtype=torch.float32)
arg_0 = arg_0_tensor.clone()
kernel_size_0 = 2
kernel_size_1 = 2
kernel_size = [kernel_size_0,kernel_size_1,]
stride_0 = 2
stride_1 = 2
stride = [stride_0,stride_1,]
padding_0 = 0
padding_1 = 0
padding = [padding_0,padding_1,]
results["res"] = torch.nn.functional.avg_pool2d(arg_0,kernel_size=kernel_size,stride=stride,padding=padding,)
