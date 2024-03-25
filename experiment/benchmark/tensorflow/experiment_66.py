results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([4], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1_tensor = tf.random.uniform([4], dtype=tf.float32)
    arg_1 = tf.identity(arg_1_tensor)
    arg_2_tensor = tf.random.uniform([4], dtype=tf.float32)
    arg_2 = tf.identity(arg_2_tensor)
    num_bits = 8
    narrow_range = False
    results["res"] = tf.quantization.fake_quant_with_min_max_vars_per_channel(arg_0,arg_1,arg_2,num_bits=num_bits,narrow_range=narrow_range,)
