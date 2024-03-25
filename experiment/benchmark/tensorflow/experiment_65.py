results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0 = 4
    arg_class = tf.keras.layers.LSTMCell(arg_0,)
    arg_input_0_tensor = tf.random.uniform([32, 8], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input_1_0_tensor = tf.random.uniform([32, 4], dtype=tf.float32)
    arg_input_1_0 = tf.identity(arg_input_1_0_tensor)
    arg_input_1_1_tensor = tf.random.uniform([32, 4], dtype=tf.float32)
    arg_input_1_1 = tf.identity(arg_input_1_1_tensor)
    arg_input_1 = [arg_input_1_0,arg_input_1_1,]
    arg_input = [arg_input_0,arg_input_1,]
    results["res"] = arg_class(*arg_input)
