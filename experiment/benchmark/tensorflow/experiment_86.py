results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    strides = 2
    filters = 2
    kernel_size = 3
    arg_class = tf.keras.layers.Convolution1DTranspose(strides=strides,filters=filters,kernel_size=kernel_size,)
    arg_input_0_tensor = tf.random.uniform([2, 6, 3], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
