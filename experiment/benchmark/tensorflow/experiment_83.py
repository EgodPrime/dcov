results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([3, 256], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    rate = 0.0
    results["res"] = tf.nn.dropout(arg_0,rate=rate,)
