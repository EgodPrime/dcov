results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([5, 10, 20], minval=-4096, maxval=8193, dtype=tf.int32)
    arg_0 = tf.identity(arg_0_tensor)
    results["res"] = tf.nn.scale_regularization_loss(arg_0,)
