# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

"""Test examples."""

import os
import subprocess
import unittest
import tensorflow as tf
import numpy as np
import tensorflow_hub as hub
import tf2onnx
import timeit
import time
import keras2onnx
import onnxruntime as rt

from onnx import helper
from tensorflow.python.keras.saving import saving_utils as _saving_utils
from tensorflow.keras import layers, models
from tensorflow import keras

from common import check_opset_min_version, check_opset_max_version, check_tf_min_version


def to_onnx(model, output=None, use_tf2onnx=True):
    if use_tf2onnx:
        function = _saving_utils.trace_model_call(model)
        concrete_func = function.get_concrete_function()

        input_names = [input_tensor.name for input_tensor in concrete_func.inputs
                       if input_tensor.dtype != tf.dtypes.resource]
        output_names = [output_tensor.name for output_tensor in concrete_func.outputs
                        if output_tensor.dtype != tf.dtypes.resource]

        frozen_graph = tf2onnx.tf_loader.from_function(concrete_func, input_names, output_names, aggressive_inlining=True)
        with tf.Graph().as_default() as tf_graph:
            tf.import_graph_def(frozen_graph, name='')

        g = tf2onnx.tfonnx.process_tf_graph(tf_graph, opset=12, input_names=input_names, output_names=output_names)
        onnx_graph = tf2onnx.optimizer.optimize_graph(g)
        model_proto = onnx_graph.make_model("test model")
    else:
        model_proto = keras2onnx.convert_keras(model, model.name)

    if output:
        tf2onnx.utils.save_protobuf(output, model_proto)

    inputs = [n.name for n in model_proto.graph.input]
    outputs = [n.name for n in model_proto.graph.output]

    return model_proto, inputs, outputs


class TestKerasApps(unittest.TestCase):

    def test_tfkeras_bert0(self):
        max_seq_length = 128
        input_word_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,
                                               name="input_word_ids")
        input_mask = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,
                                           name="input_mask")
        segment_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,
                                            name="segment_ids")
        bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_cased_L-12_H-768_A-12/2",
                                    trainable=True)

        bert_inputs = [input_word_ids, input_mask, segment_ids]
        pooled_output, sequence_output = bert_layer(bert_inputs)

        # vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
        # do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
        # tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

        model = tf.keras.models.Model(inputs=bert_inputs, outputs=[pooled_output, sequence_output])
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        in_words = np.ones([1, 128], dtype=np.int32)
        in_mask = np.ones([1, 128], dtype=np.int32)
        in_segment = np.ones([1, 128], dtype=np.int32)
        tf_ret = model.predict([in_words, in_mask, in_segment])
        N = 20
        start = time.time()
        for i in range(0, N):
            _ = model.predict([in_words, in_mask, in_segment])
        print("TF", 1000 * (time.time() - start) / N)

        model_proto, inputs, outputs = to_onnx(model, "/tmp/t.onnx", use_tf2onnx=True)
        sess = rt.InferenceSession("/tmp/t.onnx")
        feeds = {"input_word_ids:0": in_words, "input_mask:0": in_mask, "segment_ids:0": in_segment}
        onnx_ret = sess.run(outputs, feeds)
        start = time.time()
        for i in range(0, N):
            _ = sess.run(outputs, feeds)
        print("ORT", 1000 * (time.time() - start) / N)
        for i1, i2 in zip(tf_ret, onnx_ret):
            np.testing.assert_allclose(i1, i2, rtol=1e-1)


if __name__ == '__main__':
    unittest.main()
