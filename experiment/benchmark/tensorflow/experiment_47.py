results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    size_0 = 1
    size_1 = 2
    size = [size_0,size_1,]
    arg_class = tf.keras.layers.UpSampling2D(size=size,)
    arg_input_0_tensor = tf.random.uniform([2, 2, 1, 3], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
