results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    x_tensor = tf.random.uniform([1, 1, 16, 16], dtype=tf.float32)
    x = tf.identity(x_tensor)
    y_tensor = tf.random.uniform([], dtype=tf.float32)
    y = tf.identity(y_tensor)
    name = None
    results["res"] = tf.math.divide_no_nan(x=x,y=y,name=name,)
