results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([6], minval=-2, maxval=5, dtype=tf.int32)
    arg_0 = tf.identity(arg_0_tensor)
    results["res"] = tf.math.zero_fraction(arg_0,)
