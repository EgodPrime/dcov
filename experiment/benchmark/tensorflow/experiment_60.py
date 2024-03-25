results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    name = "spatial_dropout2d"
    trainable = True
    dtype = "float32"
    rate = 0.5
    noise_shape = None
    seed = None
    batch_input_shape_0 = 2
    batch_input_shape_1 = 3
    batch_input_shape_2 = 4
    batch_input_shape_3 = 5
    batch_input_shape = [batch_input_shape_0,batch_input_shape_1,batch_input_shape_2,batch_input_shape_3,]
    arg_class = tf.keras.layers.SpatialDropout2D(name=name,trainable=trainable,dtype=dtype,rate=rate,noise_shape=noise_shape,seed=seed,batch_input_shape=batch_input_shape,)
    arg_input_0_tensor = tf.random.uniform([3, 3, 4, 5], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
