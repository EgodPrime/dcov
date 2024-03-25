results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([3, 5], minval=-4, maxval=513, dtype=tf.int32)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1 = 1
    results["res"] = tf.math.argmax(arg_0,arg_1,)
