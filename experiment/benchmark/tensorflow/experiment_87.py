results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    x_0 = 0.0
    x_1 = 0.2
    x_2 = 1.0
    x_3 = 1.5
    x_4 = 2.0
    x = [x_0,x_1,x_2,x_3,x_4,]
    name = None
    results["res"] = tf.math.erfc(x=x,name=name,)
