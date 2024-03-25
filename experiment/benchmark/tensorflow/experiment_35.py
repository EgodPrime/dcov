results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([5], minval=-1, maxval=3, dtype=tf.int32)
    arg_0 = tf.identity(arg_0_tensor)
    results["res"] = tf.nn.crelu(arg_0,)
