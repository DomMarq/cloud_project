#!/afs/crc.nd.edu/user/b/bhart5/miniconda3/bin/python3

import numpy as np
import pandas as pd
import os
import tensorflow as tf
import random
import sys
from numpy import load
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
import time as timer
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# start timing 
start_train_time = timer.time()

# for xray data
data_dir = 'data/xrays/'
image_dir = data_dir + 'data/'
tfrlist_suffix = os.listdir(image_dir)
print('TFRecord file count: ' + str(len(tfrlist_suffix)))

df = pd.read_csv(data_dir + 'preprocessed_data.csv')


heads = list(df.columns)[2:]
cols = int(np.ceil(len(heads)/2))

tfrlist = [image_dir + x for x in tfrlist_suffix]

FILENAMES = tf.io.gfile.glob(tfrlist)

ALL = list(range(len(FILENAMES)))

TRAIN_AND_VALID_INDEX = random.sample(ALL, int(len(ALL) * 0.8))
TEST_INDEX = list(set(ALL) - set(TRAIN_AND_VALID_INDEX))

TRAIN_INDEX = random.sample(TRAIN_AND_VALID_INDEX, int(len(TRAIN_AND_VALID_INDEX) * 0.9))
VALID_INDEX = list(set(TRAIN_AND_VALID_INDEX) - set(TRAIN_INDEX))

TRAINING_FILENAMES, VALID_FILENAMES, TEST_FILENAMES = [FILENAMES[index] for index in TRAIN_INDEX], [FILENAMES[index] for index in VALID_INDEX], [FILENAMES[index] for index in TEST_INDEX]

print("Train TFRecord Files:", len(TRAINING_FILENAMES))
print("Validation TFRecord Files:", len(VALID_FILENAMES))
print("Test TFRecord Files:", len(TEST_FILENAMES))


feature_description = {}

for elem in list(df.columns)[2:]:
    feature_description[elem] = tf.io.FixedLenFeature([], tf.int64)

feature_description['image'] = tf.io.FixedLenFeature([], tf.string)

BATCH_SIZE = 64
IMAGE_ONE_AXIS = 100
IMAGE_SIZE = [IMAGE_ONE_AXIS, IMAGE_ONE_AXIS]
AUTOTUNE = tf.data.experimental.AUTOTUNE


def read_tfrecord(example):
    print("example:  ", example)
    example = tf.io.parse_single_example(example, feature_description)
    image = tf.io.decode_jpeg(example["image"], channels=3)
    image = tf.image.resize(image, IMAGE_SIZE)
    image = tf.cast(image, tf.float32) / 255.0

    label = []

    for val in heads: label.append(example[val])

    return image, label

def load_dataset(filenames):
    ignore_order = tf.data.Options()
    ignore_order.experimental_deterministic = False
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.with_options(ignore_order)
    dataset = dataset.map(read_tfrecord)

    return dataset

def get_dataset(filenames):
    dataset = load_dataset(filenames)
    dataset = dataset.shuffle(2048)
    dataset = dataset.prefetch(buffer_size=AUTOTUNE)
    dataset = dataset.batch(BATCH_SIZE)

    return dataset

train_dataset = get_dataset(TRAINING_FILENAMES)
valid_dataset = get_dataset(VALID_FILENAMES)
test_dataset = get_dataset(TEST_FILENAMES)

print(train_dataset)
print("test_dataset:")
print(test_dataset)
# image_viz, label_viz = next(iter(train_dataset))
# val_image_viz, val_label_viz = next(iter(valid_dataset))
#
# train_images = image_viz.numpy()
# train_labels = label_viz.numpy()
#
# # defining learning rate and early stop parameters
# initial_learning_rate = 0.01
# lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
#     initial_learning_rate, decay_steps=5, decay_rate=0.96, staircase=True
# )


# def define_model(in_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3), out_shape=len(heads)):
#     model = Sequential()
#     model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=in_shape))
#     model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
#     model.add(MaxPooling2D((2, 2)))
#     model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
#     model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
#     model.add(MaxPooling2D((2, 2)))
#     model.add(Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
#     model.add(Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
#     model.add(MaxPooling2D((2, 2)))
#     model.add(Flatten())
#     model.add(Dense(128, activation='relu', kernel_initializer='he_uniform'))
#     model.add(Dense(out_shape, activation='sigmoid'))
#
#     model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
#                   loss='binary_crossentropy',
#                   metrics=[tf.keras.metrics.AUC(name="auc")])
#     return model
#
# train_size = sum(1 for _ in tf.data.TFRecordDataset(TRAINING_FILENAMES))
# validation_size = sum(1 for _ in tf.data.TFRecordDataset(VALID_FILENAMES))


# epoch_steps = int(np.ceil(train_size/BATCH_SIZE))
# validation_steps = int(np.ceil(validation_size/BATCH_SIZE))
#
# epochs = 5
#
# print("steps_per_epoch: " + str(epoch_steps))
# print("validation_steps: " + str(validation_steps))
#
#
# # save checkpoints during training
# checkpoint_path = "training_1/cp.ckpt"
# checkpoint_dir = os.path.dirname(checkpoint_path)
#
# model_path = "saved_model"
# model_dir = os.path.dirname(model_path)

# Create a callback that saves the model's weights

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


model = define_model()

history = model.fit(
    train_dataset,
    epochs=epochs,
    validation_data=valid_dataset,
    validation_steps = validation_steps,
    callbacks=cp_callback
)

# end time
end_train_time = timer.time()
train_time = end_train_time - start_train_time
train_day = train_time // (24 * 3600)
train_time = train_time % (24 * 3600)
train_hour = train_time // 3600
train_time %= 3600
train_minutes = train_time // 60
train_time %= 60
train_seconds = np.round(train_time,0)
print(f"Total model execution time: {train_day} days, {train_hour} hours, {train_minutes} minutes, {train_seconds} seconds")

# model evaluation
start_eval_time = timer.time()
_, test_auc = model.evaluate(test_dataset, verbose=0)
print('Test auc:', test_auc)

end_eval_time = timer.time()
eval_time = end_eval_time - start_eval_time
eval_day = eval_time // (24 * 3600)
eval_time = eval_time % (24 * 3600)
eval_hour = eval_time // 3600
eval_time %= 3600
eval_minutes = eval_time // 60
eval_time %= 60
eval_seconds = np.round(eval_time,0)
print(f"Total evaluation execution time: {eval_day} days, {eval_hour} hours, {eval_minutes} minutes, {eval_seconds} seconds")


# save model
model.save('saved_model/my_model_10')

