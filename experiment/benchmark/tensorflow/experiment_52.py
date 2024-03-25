results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    rate = 0.0
    arg_class = tf.keras.layers.Dropout(rate=rate,)
    arg_input_0_tensor = tf.random.uniform([1, 5, 2, 3, 4, 3, 4], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
