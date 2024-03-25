results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    units = 4
    activation = "tanh"
    recurrent_activation = "sigmoid"
    use_bias = True
    kernel_initializer = "glorot_uniform"
    recurrent_initializer = "orthogonal"
    bias_initializer = "zeros"
    kernel_regularizer = None
    recurrent_regularizer = None
    bias_regularizer = None
    kernel_constraint = None
    recurrent_constraint = None
    bias_constraint = None
    dropout = 0.0
    recurrent_dropout = 0.0
    reset_after = True
    arg_class = tf.keras.layers.GRUCell(units=units,activation=activation,recurrent_activation=recurrent_activation,use_bias=use_bias,kernel_initializer=kernel_initializer,recurrent_initializer=recurrent_initializer,bias_initializer=bias_initializer,kernel_regularizer=kernel_regularizer,recurrent_regularizer=recurrent_regularizer,bias_regularizer=bias_regularizer,kernel_constraint=kernel_constraint,recurrent_constraint=recurrent_constraint,bias_constraint=bias_constraint,dropout=dropout,recurrent_dropout=recurrent_dropout,reset_after=reset_after,)
    arg_input_0_tensor = tf.random.uniform([32, 8], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input_1_0_tensor = tf.random.uniform([32, 4], dtype=tf.float32)
    arg_input_1_0 = tf.identity(arg_input_1_0_tensor)
    arg_input_1_1_tensor = tf.random.uniform([32, 4], dtype=tf.float32)
    arg_input_1_1 = tf.identity(arg_input_1_1_tensor)
    arg_input_1 = [arg_input_1_0,arg_input_1_1,]
    arg_input = [arg_input_0,arg_input_1,]
    results["res"] = arg_class(*arg_input)
