results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0 = 2
    arg_1 = 1000
    skip = 2
    dtype = tf.float64
    results["res"] = tf.math.sobol_sample(arg_0,arg_1,skip=skip,dtype=dtype,)
