from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
from PIL import Image as pil_image
import tensorflow
import keras

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import Model , load_model
from keras.preprocessing import image


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

Model= load_model('best_model_cutix.h5')     

class_cancer = {
    0 : 'Actinic keratoses (akiec)',
    1 : 'Basal cell carcinoma (bcc)',
    2 : 'Benign keratosis-like lesions (bkl) ',
    3 : 'Dermatofibroma (df)',
    4 : 'Melanocytic nevi (nv)',
    5 : 'Vascular lesions (vasc)',
    6 : 'Melanoma (mel)'
}

def model_predict(img_path, Model):
    img = image.load_img(img_path, target_size=(28,28,3))
  
    #img = np.asarray(pil_image.open('img').resize((120,90)))
    #x = np.asarray(img.tolist())

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    #x = preprocess_input(x, mode='caffe')

    preds = Model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path , Model)

        # Process your result for human
        

        pred_class = preds.argmax(axis=-1)            # Simple argmax
        #pred_class = decode_predictions(preds, top=1)   
        pr = class_cancer[pred_class[0]]
        result =str(pr)         
        return result
    return None


if __name__ == '__main__':
    app.run(debug=False) # Production Environment, if debug=True == Development Environment
    