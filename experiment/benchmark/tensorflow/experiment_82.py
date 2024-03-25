results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0 = 3.0
    arg_1 = 4.0
    results["res"] = tf.dtypes.complex(arg_0,arg_1,)
