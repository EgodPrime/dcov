results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([2, 16], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    seq_length = 2
    results["res"] = tf.nn.collapse_repeated(arg_0,seq_length=seq_length,)
