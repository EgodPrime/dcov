results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_0 = 2
    arg_0_1 = 3
    arg_0 = [arg_0_0,arg_0_1,]
    arg_1 = 2.0
    arg_2 = 0.5
    results["res"] = tf.random.gamma(arg_0,arg_1,arg_2,)
