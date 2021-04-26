import os

import tensorflow as tf
from tensorflow import keras
import numpy as np
# pip install Pillow
# in prod, this wouldn't need to be imported ideally
import PIL

print(tf.version.VERSION)

new_model = tf.keras.models.load_model('saved_model/my_model')

# Check its architecture
new_model.summary()
IMAGE_ONE_AXIS = 100
IMAGE_SIZE = [IMAGE_ONE_AXIS, IMAGE_ONE_AXIS]



# _, test_auc = model.evaluate(test_dataset, verbose=0)
# print('Test auc:', test_auc)

def read_tfrecord(image):
    image = tf.io.decode_image(image, expand_animations=True)
    image = tf.image.resize(image, IMAGE_SIZE)
    image = tf.cast(image, tf.float32) / 255.0

    return image

data_dir = 'data/xrays/'
image_dir = data_dir + 'raw_images/'
filename = image_dir + "00000001_000.png"

data = PIL.Image.open(filename)
data = read_tfrecord(data)

results = new_model.predict(data, use_multiprocessing=True)
print(results)
#
# def load_dataset(filenames):
#     ignore_order = tf.data.Options()
#     ignore_order.experimental_deterministic = False
#     dataset = tf.data.TFRecordDataset(filenames)
#     dataset = dataset.with_options(ignore_order)
#     dataset = dataset.map(read_tfrecord)
#
#     return dataset
#
# def get_dataset(filenames):
#     dataset = load_dataset(filenames)
#     dataset = dataset.shuffle(2048)
#     dataset = dataset.prefetch(buffer_size=AUTOTUNE)
#     dataset = dataset.batch(BATCH_SIZE)
#
#     return dataset
#
# train_dataset = get_dataset(TRAINING_FILENAMES)
# valid_dataset = get_dataset(VALID_FILENAMES)
# test_dataset = get_dataset(TEST_FILENAMES)
