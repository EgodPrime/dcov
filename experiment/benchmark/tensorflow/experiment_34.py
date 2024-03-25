results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_0_0 = 1
    arg_0_0_1 = 2
    arg_0_0_2 = 3
    arg_0_0 = [arg_0_0_0,arg_0_0_1,arg_0_0_2,]
    arg_0_1_0 = 4
    arg_0_1_1 = 5
    arg_0_1 = [arg_0_1_0,arg_0_1_1,]
    arg_0_2_0 = 6
    arg_0_2_1 = 7
    arg_0_2_2 = 8
    arg_0_2_3 = 9
    arg_0_2 = [arg_0_2_0,arg_0_2_1,arg_0_2_2,arg_0_2_3,]
    arg_0 = [arg_0_0,arg_0_1,arg_0_2,]
    results["res"] = tf.ragged.constant(arg_0,)
