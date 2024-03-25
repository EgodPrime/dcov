results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    input_tensor_tensor = tf.cast(tf.random.uniform([1, 512], minval=0, maxval=2, dtype=tf.int32), dtype=tf.bool)
    input_tensor = tf.identity(input_tensor_tensor)
    axis = None
    keepdims = False
    name = None
    results["res"] = tf.math.reduce_all(input_tensor=input_tensor,axis=axis,keepdims=keepdims,name=name,)
