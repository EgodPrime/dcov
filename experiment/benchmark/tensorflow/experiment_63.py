results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    name = "conv3d_transpose"
    trainable = True
    dtype = "float32"
    filters = 2
    kernel_size_0 = 3
    kernel_size_1 = 3
    kernel_size_2 = 3
    kernel_size = [kernel_size_0,kernel_size_1,kernel_size_2,]
    strides_0 = 1
    strides_1 = 1
    strides_2 = 1
    strides = [strides_0,strides_1,strides_2,]
    padding = "same"
    data_format = "channels_last"
    groups = 1
    activation = "linear"
    use_bias = True
    kernel_initializer = None
    bias_initializer = None
    kernel_regularizer = None
    bias_regularizer = None
    activity_regularizer = None
    kernel_constraint = None
    bias_constraint = None
    output_padding = None
    batch_input_shape_0 = 2
    batch_input_shape_1 = 5
    batch_input_shape_2 = 7
    batch_input_shape_3 = 6
    batch_input_shape_4 = 3
    batch_input_shape = [batch_input_shape_0,batch_input_shape_1,batch_input_shape_2,batch_input_shape_3,batch_input_shape_4,]
    arg_class = tf.keras.layers.Convolution3DTranspose(name=name,trainable=trainable,dtype=dtype,filters=filters,kernel_size=kernel_size,strides=strides,padding=padding,data_format=data_format,groups=groups,activation=activation,use_bias=use_bias,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer,kernel_regularizer=kernel_regularizer,bias_regularizer=bias_regularizer,activity_regularizer=activity_regularizer,kernel_constraint=kernel_constraint,bias_constraint=bias_constraint,output_padding=output_padding,batch_input_shape=batch_input_shape,)
    arg_input_0_tensor = tf.random.uniform([3, 5, 7, 6, 3], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
