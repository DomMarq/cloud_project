import os
import sys
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np

#print(tf.version.VERSION)
new_model = tf.keras.models.load_model('saved_model/my_model')

# Check its architecture
new_model.summary()
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
image_dir = data_dir + 'raw_images/'
filename = image_dir + image_name

# Process data
data = tf.io.read_file(filename)
data = read_tfrecord(data)

# Call model on data
results = new_model.predict(data, use_multiprocessing=True)
#print('\n------------------------------------------------')
#print('Probabilities:')
#print(results)

# determine max prob, change to say yes for all probs over 0.1?
maximum = np.argmax(results)
options = list(df.columns)[2:]
#print("\nDiagnosis:")
#print(options[maximum])
#print(maximum)
f = open('output.txt', 'a')
f.write(str(maximum))
f.write('\n')
f.close()
#for i, row in df.iterrows():
#    if image_name == row[0][-16:]:
#        # check for correctness
#        for i, col in enumerate(row):
#            if i-2 == maximum:
#                if col:
#                    print('\nCorrect prediction!')
#                else:
#                    print('\nIncorrect prediction!')
#                print('------------------------------------------------')

