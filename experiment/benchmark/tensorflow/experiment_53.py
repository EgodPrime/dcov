results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    x_tensor = tf.random.uniform([6], dtype=tf.float32)
    x = tf.identity(x_tensor)
    name = None
    results["res"] = tf.math.floor(x=x,name=name,)
