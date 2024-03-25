results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.complex(tf.random.uniform([2, 2], dtype=tf.float32),tf.random.uniform([2, 2], dtype=tf.float32))
    arg_0 = tf.identity(arg_0_tensor)
    results["res"] = tf.linalg.logm(arg_0,)
