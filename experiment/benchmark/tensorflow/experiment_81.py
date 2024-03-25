results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    labels_tensor = tf.random.uniform([3, 2], minval=-256, maxval=513, dtype=tf.int32)
    labels = tf.identity(labels_tensor)
    logits_tensor = tf.random.uniform([3, 10, 5], dtype=tf.float32)
    logits = tf.identity(logits_tensor)
    label_length_tensor = tf.random.uniform([3], minval=-8, maxval=513, dtype=tf.int32)
    label_length = tf.identity(label_length_tensor)
    logit_length_tensor = tf.random.uniform([3], minval=-2, maxval=4097, dtype=tf.int32)
    logit_length = tf.identity(logit_length_tensor)
    logits_time_major = False
    blank_index = -1
    results["res"] = tf.nn.ctc_loss(labels=labels,logits=logits,label_length=label_length,logit_length=logit_length,logits_time_major=logits_time_major,blank_index=blank_index,)
