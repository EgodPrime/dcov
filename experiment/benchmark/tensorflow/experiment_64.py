results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([1, 1, 3, 3], dtype=tf.float16)
    arg_0 = tf.identity(arg_0_tensor)
    ksize = 2
    strides_0 = 1
    strides_1 = 2
    strides_2 = 2
    strides_3 = 1
    strides = [strides_0,strides_1,strides_2,strides_3,]
    padding = "SAME"
    results["res"] = tf.nn.avg_pool2d(arg_0,ksize=ksize,strides=strides,padding=padding,)
