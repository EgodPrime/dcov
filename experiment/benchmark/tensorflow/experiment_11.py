results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0 = 0.1
    dtype = None
    arg_class = tf.keras.layers.GaussianDropout(arg_0,dtype=dtype,)
    arg_input_0_tensor = tf.random.uniform([8, 8], dtype=tf.float64)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
