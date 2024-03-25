results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    x_tensor = tf.random.uniform([], dtype=tf.float32)
    x = tf.identity(x_tensor)
    y_tensor = tf.random.uniform([], dtype=tf.float32)
    y = tf.identity(y_tensor)
    results["res"] = tf.raw_ops.AddV2(x=x,y=y,)
