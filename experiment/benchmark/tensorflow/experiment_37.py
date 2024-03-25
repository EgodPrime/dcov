results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    name = "average_pooling1d"
    trainable = True
    dtype = "float32"
    strides_0 = 1
    strides = [strides_0,]
    pool_size_0 = 2
    pool_size = [pool_size_0,]
    padding = "valid"
    data_format = "channels_last"
    batch_input_shape_0 = 3
    batch_input_shape_1 = 5
    batch_input_shape_2 = 4
    batch_input_shape = [batch_input_shape_0,batch_input_shape_1,batch_input_shape_2,]
    arg_class = tf.keras.layers.AvgPool1D(name=name,trainable=trainable,dtype=dtype,strides=strides,pool_size=pool_size,padding=padding,data_format=data_format,batch_input_shape=batch_input_shape,)
    arg_input_0_tensor = tf.random.uniform([1, 5, 4], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
