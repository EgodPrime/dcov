results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([6], minval=-4, maxval=8193, dtype=tf.int32)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1_tensor = tf.random.uniform([6], minval=-2, maxval=3, dtype=tf.int32)
    arg_1 = tf.identity(arg_1_tensor)
    num_segments = 3
    results["res"] = tf.math.unsorted_segment_sum(arg_0,arg_1,num_segments=num_segments,)
