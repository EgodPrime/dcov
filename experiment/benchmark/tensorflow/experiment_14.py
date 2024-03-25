results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([2, 3], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    axis = 1
    results["res"] = tf.nn.isotonic_regression(arg_0,axis=axis,)
