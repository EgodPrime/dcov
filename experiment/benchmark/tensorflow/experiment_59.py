results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    layer = None
    results["res"] = tf.keras.layers.serialize(layer=layer,)
