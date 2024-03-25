results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    input_tensor = tf.cast(tf.random.uniform([3, 3], minval=0, maxval=2, dtype=tf.int32), dtype=tf.bool)
    input = tf.identity(input_tensor)
    axis = -1
    results["res"] = tf.raw_ops.All(input=input,axis=axis,)
