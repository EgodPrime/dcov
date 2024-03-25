results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    alpha = 0.1
    arg_class = tf.keras.layers.LeakyReLU(alpha=alpha,)
    arg_input_0_0 = -3.0
    arg_input_0_1 = -1.0
    arg_input_0_2 = 0.0
    arg_input_0_3 = 2.0
    arg_input_0 = [arg_input_0_0,arg_input_0_1,arg_input_0_2,arg_input_0_3,]
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
