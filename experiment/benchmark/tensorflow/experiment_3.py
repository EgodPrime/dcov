results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    x = 0.0
    y = 1.0
    name = None
    results["res"] = tf.math.xdivy(x=x,y=y,name=name,)
