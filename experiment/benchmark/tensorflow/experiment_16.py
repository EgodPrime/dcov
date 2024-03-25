results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_0_tensor = tf.random.uniform([], dtype=tf.float32)
    arg_0_0 = tf.identity(arg_0_0_tensor)
    arg_0_1_tensor = tf.random.uniform([], dtype=tf.float32)
    arg_0_1 = tf.identity(arg_0_1_tensor)
    arg_0 = [arg_0_0,arg_0_1,]
    results["res"] = tf.math.add_n(arg_0,)
