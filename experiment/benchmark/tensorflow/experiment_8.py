results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    x_tensor = tf.random.uniform([3], dtype=tf.float32)
    x = tf.identity(x_tensor)
    name = None
    results["res"] = tf.math.expm1(x=x,name=name,)
