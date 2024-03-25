results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([1, 64, 64, 32], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1_tensor = tf.random.uniform([5, 5, 32, 2], dtype=tf.float32)
    arg_1 = tf.identity(arg_1_tensor)
    strides_0 = 1
    strides_1 = 2
    strides_2 = 2
    strides_3 = 1
    strides = [strides_0,strides_1,strides_2,strides_3,]
    padding = "SAME"
    results["res"] = tf.nn.depthwise_conv2d(arg_0,arg_1,strides=strides,padding=padding,)
