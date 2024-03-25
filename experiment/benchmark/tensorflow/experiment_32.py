results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    filters = 4
    kernel_size = 2
    arg_class = tf.keras.layers.Convolution2D(filters=filters,kernel_size=kernel_size,)
    arg_input_0_tensor = tf.random.uniform([4, 4, 4, 4], dtype=tf.float64)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
