results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    pool_size_0 = 2
    pool_size_1 = 2
    pool_size = [pool_size_0,pool_size_1,]
    input_shape_0 = 4
    input_shape_1 = 4
    input_shape_2 = 1
    input_shape = [input_shape_0,input_shape_1,input_shape_2,]
    arg_class = tf.keras.layers.MaxPool2D(pool_size=pool_size,input_shape=input_shape,)
    arg_input_0_tensor = tf.random.uniform([1, 4, 4, 1], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
