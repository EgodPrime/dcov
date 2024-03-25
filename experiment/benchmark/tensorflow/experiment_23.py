results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    starts_0 = 1
    starts_1 = 3
    starts_2 = 6
    starts = [starts_0,starts_1,starts_2,]
    limits_0 = 4
    limits_1 = 7
    limits_2 = 9
    limits = [limits_0,limits_1,limits_2,]
    results["res"] = tf.ragged.range(starts=starts,limits=limits,)
