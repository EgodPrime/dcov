results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    name = "locally_connected2d_1"
    trainable = True
    dtype = "float32"
    filters = 3
    kernel_size_0 = 3
    kernel_size_1 = 3
    kernel_size = [kernel_size_0,kernel_size_1,]
    strides_0 = 2
    strides_1 = 2
    strides = [strides_0,strides_1,]
    padding = "valid"
    data_format = "channels_first"
    activation = "linear"
    use_bias = True
    kernel_initializer = None
    bias_initializer = None
    kernel_regularizer = None
    bias_regularizer = None
    activity_regularizer = None
    kernel_constraint = None
    bias_constraint = None
    implementation = 3
    arg_class = tf.keras.layers.LocallyConnected2D(name=name,trainable=trainable,dtype=dtype,filters=filters,kernel_size=kernel_size,strides=strides,padding=padding,data_format=data_format,activation=activation,use_bias=use_bias,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer,kernel_regularizer=kernel_regularizer,bias_regularizer=bias_regularizer,activity_regularizer=activity_regularizer,kernel_constraint=kernel_constraint,bias_constraint=bias_constraint,implementation=implementation,)
    arg_input_0_tensor = tf.random.uniform([3, 6, 10, 4], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
