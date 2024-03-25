results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    x_tensor = tf.random.uniform([4], minval=-256, maxval=17, dtype=tf.int32)
    x = tf.identity(x_tensor)
    axis = 0
    exclusive = True
    reverse = True
    name = None
    results["res"] = tf.math.cumprod(x=x,axis=axis,exclusive=exclusive,reverse=reverse,name=name,)
