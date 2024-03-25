results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([3], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1 = 2
    arg_2 = 3
    results["res"] = tf.math.betainc(arg_0,arg_1,arg_2,)
