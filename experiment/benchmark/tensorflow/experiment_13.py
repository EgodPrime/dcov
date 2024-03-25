results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.saturate_cast(tf.random.uniform([3], minval=0, maxval=2, dtype=tf.int64), dtype=tf.uint8)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1 = 2
    results["res"] = tf.bitwise.left_shift(arg_0,arg_1,)
