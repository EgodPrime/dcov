results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([2, 1], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    results["res"] = tf.math.sqrt(arg_0,)
