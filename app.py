import base64
import numpy as np
import io
import h5py
from PIL import Image
import keras
import tensorflow as tf
from keras import backend as K
from keras.models import Sequential
from tensorflow.python.keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask, render_template, redirect, url_for, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)
# cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})
heroku = Heroku(app)
db = SQLAlchemy(app)


class Survey(db.Model):
    __tablename__ = "surveys"
    id = db.Column(db.Integer, primary_key = True)
    age = db.Column(db.Integer)
    location = db.Column(db.String(120))
    education = db.Column(db.String(25))
    gender = db.Column(db.String(10))
    realWidth = db.Column(db.Integer)
    realHeight = db.Column(db.Integer)
    pred1 = db.Column(db.String(10))
    pred2 = db.Column(db.String(10))
    pred3 = db.Column(db.String(10))
    pred4 = db.Column(db.String(10))
    pred5 = db.Column(db.Integer)

    def __init__(self, age, location, education, gender, pred1, pred2, pred3, pred4, pred5, realWidth, realHeight):
        self.age = age
        self.location = location
        self.education = education
        self.gender = gender
        self.realWidth = realWidth
        self.realHeight = realHeight
        self.pred1 = pred1
        self.pred2 = pred2
        self.pred3 = pred3
        self.pred4 = pred4
        self.pred5 = pred5


def get_model():
	global model
	model = load_model('Model_Filter_classifier-8_ResNet_Original_vs_Filtered_32x32-20-0.8903.h5')
	print(" * Model Loaded!")
	model._make_predict_function()

def preprocess_image(image, target_size):
	if image.mode != "RGB":
		image = image.convert("RGB")
	image = image.resize(target_size, Image.LANCZOS)
	image = img_to_array(image)
	image = np.expand_dims(image, axis = 0)
	image = image.astype('float32') / 255
	
	return image
	
print(" * Loading Model...")
get_model()

@app.route('/')
@app.route('/home')
def home_function():
	print("In home function")
	return render_template('home.html')


@app.route('/predict', methods = ['GET', 'POST'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])

def predict_function():
	print("In predict function")
	message = request.get_json(force = True)
	encoded = message['image']
	
	decoded = base64.b64decode(encoded)
	image = Image.open(io.BytesIO(decoded))
	processed_image = preprocess_image(image, target_size = (32, 32))
	
	prediction = model.predict(processed_image).tolist()
	
	response = {
		'prediction': {
			'original': prediction[0][0],
			'filtered': prediction[0][1]
		}
	}
	
	print(response)
	
	
	return jsonify(response)

@app.route('/store', methods = ['GET', 'POST'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])

def store_function():
	print("In store function")
	userInfo = request.get_json(force = True)
	age = userInfo['age']
	location = userInfo['location']
	education = userInfo['education']
	gender = userInfo['gender']
	pred1 = userInfo['pred1']
	pred2 = userInfo['pred2']
	pred3 = userInfo['pred3']
	pred4 = userInfo['pred4']
	pred5 = userInfo['pred5']
	realWidth = userInfo['realWidth']
	realHeight = userInfo['realHeight'] 
    
	print(age)
	print(location)
	print(education)
	print(gender)
	print(pred1)
	print(pred2)
	print(pred3)
	print(pred4)
	print(pred5)
	print(realWidth)
	print(realHeight)


	survey = Survey(age, location, education, gender, pred1, pred2, pred3, pred4, pred5, realWidth, realHeight)
	db.session.add(survey)
	db.session.commit()

	return jsonify(userInfo)


if __name__ == "__main__":
	app.run(debug = True)