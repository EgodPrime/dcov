results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    counts_tensor = tf.random.uniform([2, 1, 1, 3, 3], dtype=tf.float32)
    counts = tf.identity(counts_tensor)
    mean_ss = 0
    variance_ss = False
    shift = None
    name = None
    results["res"] = tf.nn.normalize_moments(counts=counts,mean_ss=mean_ss,variance_ss=variance_ss,shift=shift,name=name,)
