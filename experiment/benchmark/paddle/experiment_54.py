results = dict()
import paddle

paddle.device.set_device("cpu")
reduction = "none"
arg_class = paddle.nn.TripletMarginLoss(reduction=reduction,)
arg_input_0_tensor = paddle.uniform(shape = [3, 3],min = -2048,max = 2048)
arg_input_0 = paddle.cast(arg_input_0_tensor,paddle.float32)
arg_input_1_tensor = paddle.uniform(shape = [3, 3],min = -4096,max = 32)
arg_input_1 = paddle.cast(arg_input_1_tensor,paddle.float32)
arg_input_2_tensor = paddle.uniform(shape = [3, 3],min = -1,max = 1)
arg_input_2 = paddle.cast(arg_input_2_tensor,paddle.float32)
arg_input = [arg_input_0,arg_input_1,arg_input_2,]
results["res"] = arg_class(*arg_input)
