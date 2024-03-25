results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    arg_0 = 32
    arg_1 = 3
    activation = "relu"
    input_shape_0 = 10
    input_shape_1 = 128
    input_shape = [input_shape_0,input_shape_1,]
    arg_class = tf.keras.layers.Conv1D(arg_0,arg_1,activation=activation,input_shape=input_shape,)
    arg_input_0_tensor = tf.random.uniform([4, 10, 128], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
