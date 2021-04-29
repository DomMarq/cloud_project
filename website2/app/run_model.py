import os
import sys
import pandas as pd
import tensorflow as tf
from tensorflow import keras

# print(tf.version.VERSION)
new_model = tf.keras.models.load_model('saved_model/my_model')

# Check its architecture
# new_model.summary()
IMAGE_ONE_AXIS = 100
IMAGE_SIZE = [IMAGE_ONE_AXIS, IMAGE_ONE_AXIS]

# Features
data_dir = 'data/xrays/'
df = pd.read_csv(data_dir + 'preprocessed_data.csv')

# Command line arguments
image_name = ''
try:
    image_name = sys.argv[1]
except:
    print('Error: Please enter image file')
    sys.exit()

def read_tfrecord(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, IMAGE_SIZE)
    image = tf.cast(image, tf.float32) / 255.0
    image = image[None,:,:,:]
    return image

# Directories
data_dir = 'data/xrays/'
# image_dir = data_dir + 'raw_images/'
# filename = image_dir + image_name
filename = image_name

# Process data
data = tf.io.read_file(filename)
data = read_tfrecord(data)

# Call model on data
results = new_model.predict(data, use_multiprocessing=True)

options = list(df.columns)[2:]
diagnosis = []

# 0.17 minimum
for i, result in enumerate(results[0]):
    if result >= 0.17:
        diagnosis.append(options[i])

if not diagnosis:
    diagnosis.append('No finding')

print(diagnosis)
