results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.complex(tf.random.uniform([3], dtype=tf.float64),tf.random.uniform([3], dtype=tf.float64))
    arg_0 = tf.identity(arg_0_tensor)
    results["res"] = tf.math.imag(arg_0,)
