results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    input_tensor = tf.random.uniform([1, 118, 124, 256], dtype=tf.float32)
    input = tf.identity(input_tensor)
    block_size = 2
    data_format = "NHWC"
    name = None
    results["res"] = tf.nn.space_to_depth(input=input,block_size=block_size,data_format=data_format,name=name,)
