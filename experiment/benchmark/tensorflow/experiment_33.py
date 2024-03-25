results = dict()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

with tf.device('/cpu'):
    max_tokens = None
    num_oov_indices = 1
    mask_token = None
    oov_token = -1
    vocabulary_0 = 12
    vocabulary_1 = 36
    vocabulary_2 = 1138
    vocabulary_3 = 42
    vocabulary = [vocabulary_0,vocabulary_1,vocabulary_2,vocabulary_3,]
    idf_weights = None
    invert = True
    output_mode = "int"
    sparse = False
    pad_to_max_tokens = False
    arg_class = tf.keras.layers.IntegerLookup(max_tokens=max_tokens,num_oov_indices=num_oov_indices,mask_token=mask_token,oov_token=oov_token,vocabulary=vocabulary,idf_weights=idf_weights,invert=invert,output_mode=output_mode,sparse=sparse,pad_to_max_tokens=pad_to_max_tokens,)
    arg_input_0_tensor = tf.random.uniform([2, 3], minval=-8, maxval=1025, dtype=tf.int32)
    arg_input_0 = tf.identity(arg_input_0_tensor)
    arg_input = [arg_input_0,]
    results["res"] = arg_class(*arg_input)
