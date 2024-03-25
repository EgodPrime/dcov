results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([1, 4, 2], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1_tensor = tf.random.uniform([1, 2, 2], dtype=tf.float32)
    arg_1 = tf.identity(arg_1_tensor)
    output_shape_0 = 1
    output_shape_1 = 8
    output_shape_2 = 2
    output_shape = [output_shape_0,output_shape_1,output_shape_2,]
    strides = 2
    padding = "SAME"
    results["res"] = tf.nn.conv1d_transpose(arg_0,arg_1,output_shape=output_shape,strides=strides,padding=padding,)
