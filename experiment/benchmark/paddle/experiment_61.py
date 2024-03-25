results = dict()
import paddle

paddle.device.set_device("cpu")
input_tensor = paddle.uniform(shape = [2, 2],min = -8,max = 64)
input = paddle.cast(input_tensor,paddle.float32)
x_tensor = paddle.uniform(shape = [2, 2],min = -8192,max = 8192)
x = paddle.cast(x_tensor,paddle.float32)
y_tensor = paddle.uniform(shape = [2, 2],min = -32,max = 32)
y = paddle.cast(y_tensor,paddle.float32)
beta = 0.5
alpha = 5.0
results["res"] = paddle.addmm(input=input,x=x,y=y,beta=beta,alpha=alpha,)
