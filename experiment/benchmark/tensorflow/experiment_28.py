results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([1, 2, 2, 3], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    ksize = 1024
    strides = 1024
    padding = "VALID"
    results["res"] = tf.nn.max_pool2d(arg_0,ksize=ksize,strides=strides,padding=padding,)
