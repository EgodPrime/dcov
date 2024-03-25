results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([1, 118, 124, 256], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1 = 2
    results["res"] = tf.nn.depth_to_space(arg_0,arg_1,)
