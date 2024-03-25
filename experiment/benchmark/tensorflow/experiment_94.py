results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([4], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    arg_1 = -2.0
    arg_2 = 2.0
    num_bits = 8
    results["res"] = tf.quantization.fake_quant_with_min_max_args(arg_0,arg_1,arg_2,num_bits=num_bits,)
