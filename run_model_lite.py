import os
import sys
import json
from tflite_runtime.interpreter import Interpreter
import numpy as np
from PIL import Image

# Import model lite
interpreter = Interpreter('saved_model_lite/model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()[0]
input_index = input_details['index']
input_shape = input_details['shape']
input_height = input_shape[1]
input_width = input_shape[2]
output_details = interpreter.get_output_details()[0]
output_index = output_details['index']

# Command line arguments
image_name = ''
try:
    image_name = sys.argv[1]
except:
    print('Error: Please enter image file')
    sys.exit()

# Directories
filename = 'data/xrays/raw_images/' + image_name

# Process data
xray_image = Image.open(filename)
xray_image = xray_image.convert('RGB').resize((input_width, input_height))
input_image = np.asarray(xray_image.getdata(), dtype=np.float32).reshape((1, input_width, input_height, 3)) / 255.0

interpreter.set_tensor(input_index, input_image)
interpreter.invoke()
output = interpreter.get_tensor(output_index)

options = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax', 'Edema', 'Emphysema', 'Fibrosis', 'Effusion', 'Pneumonia', 'Pleural Thickening', 'Cardiomegaly', 'Nodule', 'Mass', 'Hernia']

thresholds = [0.097, 0.034, 0.17, 0.045, 0.016, 0.019, 0.0124, 0.094, 0.01, 0.024, 0.02, 0.043, 0.041, 0.001]

diagnosis = []

for i, probability in enumerate(output[0]):
    if probability >= thresholds[i]:
        diagnosis.append(options[i])

if not diagnosis:
    diagnosis.append('No finding')

print(json.dumps({'diagnosis' : diagnosis}))

