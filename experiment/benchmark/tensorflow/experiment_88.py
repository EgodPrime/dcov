results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    name = "spatial_dropout1d"
    trainable = True
    dtype = "float32"
    rate = 0.5
    noise_shape = None
    seed = None
    arg_class = tf.keras.layers.SpatialDropout1D(name=name,trainable=trainable,dtype=dtype,rate=rate,noise_shape=noise_shape,seed=seed,)
    arg_input_0_tensor = tf.random.uniform([1, 3, 4], dtype=tf.float32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
