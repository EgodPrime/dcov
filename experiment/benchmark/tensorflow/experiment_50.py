results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    input_tensor = tf.random.uniform([2, 3], minval=-4, maxval=65, dtype=tf.int32)
    input = tf.identity(input_tensor)
    dimension = 1
    results["res"] = tf.raw_ops.ArgMax(input=input,dimension=dimension,)
