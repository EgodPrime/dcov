results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    x_0 = -1.0
    x_1 = -0.1
    x_2 = 0.1
    x_3 = 1.0
    x = [x_0,x_1,x_2,x_3,]
    name = None
    results["res"] = tf.math.sin(x=x,name=name,)
