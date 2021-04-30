import os
import sys
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np

# open tensorflow model
model = tf.keras.models.load_model('saved_model/my_model')

# convert to tensorflow lite model
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# save tensorflow lite model
with open('saved_model_lite/model.tflite', 'wb') as output:
    output.write(tflite_model)
