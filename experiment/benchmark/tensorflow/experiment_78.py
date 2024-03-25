results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    strides = 3
    padding = "valid"
    data_format = "channels_first"
    pool_size_0 = 3
    pool_size_1 = 3
    pool_size_2 = 3
    pool_size = [pool_size_0,pool_size_1,pool_size_2,]
    arg_class = tf.keras.layers.MaxPooling3D(strides=strides,padding=padding,data_format=data_format,pool_size=pool_size,)
    arg_input_0_tensor = tf.random.uniform([1, 4, 11, 12, 10], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
