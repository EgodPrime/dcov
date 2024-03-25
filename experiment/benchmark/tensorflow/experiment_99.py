results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_class = tf.keras.layers.GlobalMaxPooling2D()
    arg_input_0_tensor = tf.random.uniform([2, 4, 5, 3], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
