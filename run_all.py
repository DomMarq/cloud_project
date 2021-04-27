import os
import sys
#import pandas as pd
#import tensorflow as tf
#from tensorflow import keras
#import numpy as np
#import prediction.py 


# Features
data_dir = 'data/xrays/'
#df = pd.read_csv(data_dir + 'preprocessed_data.csv')

# Directories
data_dir = 'data/xrays/'
image_dir = data_dir + 'raw_images/'
#filename = image_dir + image_name

images = os.listdir(image_dir)
for image in images:
    #filename = image_dir + image
    command = 'python prediction.py ' + image
    #+ ' >>output.txt 2>&1'
    os.system(command)
    print(command)

print('all finsihed')
