results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_0 = 0.0
    arg_0_1 = 0.2
    arg_0_2 = 1.0
    arg_0_3 = 1.5
    arg_0_4 = 2.0
    arg_0 = [arg_0_0,arg_0_1,arg_0_2,arg_0_3,arg_0_4,]
    results["res"] = tf.math.erfcinv(arg_0,)
