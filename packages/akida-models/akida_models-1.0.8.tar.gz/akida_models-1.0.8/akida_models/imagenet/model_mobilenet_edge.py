#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
This model is an adaptation of the `mobilenet_imagenet` model for edge
applications. It is based on MobileNetBC with top layers replaced by a quantized
spike extractor and a classification layer.

It comes with a `mobilenet_edge_imagenet_pretrained` helper method that loads a
set of pretrained weights on a Mobilenet 0.5 that can be run on Akida hardware.
"""

# Tensorflow/Keras imports
from tensorflow.keras import Model
from tensorflow.keras.utils import get_file
from tensorflow.keras.layers import Reshape, Activation

# CNN2SNN imports
from cnn2snn import load_quantized_model, quantize_layer

# Local utils
from ..layer_blocks import separable_conv_block, dense_block

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/mobilenet_edge/'


def mobilenet_edge_imagenet(base_model, classes):
    """Instantiates a MobileNet-edge architecture.

    Args:
        base_model (str/tf.keras.Model): a mobilenet_imagenet quantized model.
        classes (int) : the number of classes for the edge classifier.

    Returns:
        tf.keras.Model: a Keras Model instance.
    """
    if isinstance(base_model, str):
        base_model = load_quantized_model(base_model)

    try:
        # Identify the last separable, which is the base model classifier
        base_classifier = base_model.get_layer("separable_14")
        # remember the classifier weight bitwidth
        wq = base_classifier.quantizer.bitwidth
    except:
        raise ValueError(
            "The base model is not a quantized Mobilenet/Imagenet model")

    # Recreate a model with all layers up to the classifier
    x = base_classifier.input
    # Add the new end layer with kernel_size (3, 3) instead of (1,1) for
    # hardware compatibility reasons
    x = separable_conv_block(x,
                             filters=2048,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             name='spike_generator',
                             add_activation=True)

    # Then add the Akida edge learning layer that will be dropped after
    x = dense_block(x,
                    classes,
                    name="classification_layer",
                    add_activation=False,
                    add_batchnorm=False,
                    use_bias=False)
    x = Activation('softmax', name='act_softmax')(x)
    x = Reshape((classes,), name='reshape_2')(x)

    # Create model
    model = Model(inputs=base_model.input,
                  outputs=x,
                  name=f"{base_model.name}_edge")

    # Quantize edge layers
    model = quantize_layer(model, 'spike_generator', wq)
    model = quantize_layer(model, 'spike_generator_relu', 1)
    # NOTE: quantization set to 2 here, to be as close as
    # possible to the Akida native layer that will replace this one,
    # with binary weights.
    model = quantize_layer(model, 'classification_layer', 2)

    return model


def mobilenet_edge_imagenet_pretrained():
    model_name = 'mobilenet_imagenet_alpha_50_edge_iq8_wq4_aq4.h5'
    file_hash = '707B9061CF60EC38D17ABF60AFFA0108E5B8C7E58F076347490ADEC2685F7A0D'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)
