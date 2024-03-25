results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([2, 2], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1_tensor = tf.random.uniform([2, 2], dtype=tf.float32)
    arg_1 = tf.identity(arg_1_tensor)
    results["res"] = tf.linalg.matmul(arg_0,arg_1,)
