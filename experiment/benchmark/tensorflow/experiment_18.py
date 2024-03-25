results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_class = tf.keras.layers.Minimum()
    arg_input_0_0_tensor = tf.random.uniform([5, 8], dtype=tf.float32)
    arg_input_0_0 = tf.identity(arg_input_0_0_tensor)
    arg_input_0_1_tensor = tf.random.uniform([5, 8], dtype=tf.float32)
    arg_input_0_1 = tf.identity(arg_input_0_1_tensor)
    arg_input_0 = [arg_input_0_0,arg_input_0_1,]
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
