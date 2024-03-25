results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.cast(tf.random.uniform([1], minval=0, maxval=2, dtype=tf.int32), dtype=tf.bool)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1_tensor = tf.cast(tf.random.uniform([4], minval=0, maxval=2, dtype=tf.int32), dtype=tf.bool)
    arg_1 = tf.identity(arg_1_tensor)
    results["res"] = tf.math.logical_xor(arg_0,arg_1,)
