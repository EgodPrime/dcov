results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    name = "p_re_lu"
    trainable = True
    batch_input_shape_0 = 2
    batch_input_shape_1 = 3
    batch_input_shape_2 = 4
    batch_input_shape = [batch_input_shape_0,batch_input_shape_1,batch_input_shape_2,]
    dtype = "float32"
    alpha_initializer = None
    alpha_regularizer = None
    alpha_constraint = None
    shared_axes = None
    arg_class = tf.keras.layers.PReLU(name=name,trainable=trainable,batch_input_shape=batch_input_shape,dtype=dtype,alpha_initializer=alpha_initializer,alpha_regularizer=alpha_regularizer,alpha_constraint=alpha_constraint,shared_axes=shared_axes,)
    arg_input_0_tensor = tf.random.uniform([1, 3, 4], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
