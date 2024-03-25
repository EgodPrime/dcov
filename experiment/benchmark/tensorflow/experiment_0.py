results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0_tensor = tf.random.uniform([3, 3], dtype=tf.float32)
    arg_0 = tf.identity(arg_0_tensor)
    num_samples = 5
    results["res"] = tf.random.categorical(arg_0,num_samples=num_samples,)
