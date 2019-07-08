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
from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
# cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

def get_model():
	global model
	model = load_model('Model_original_vs_filtered_zero_shot_nashville_toaster_End_to_end-5_with_sepia-10-0.8510.h5')
	print(" * Model Loaded!")
	model._make_predict_function()

def preprocess_image(image, target_size):
	if image.mode != "RGB":
		image = image.convert("RGB")
	image = image.resize(target_size, Image.ANTIALIAS)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = image.astype('float32') / 255
	
	return image
	
print(" * Loading Model...")
get_model()


@app.route("/predict", methods=["POST"])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])

def predict():
	print("In index function")
	message = request.get_json(force=True)
	encoded = message['image']
	
	decoded = base64.b64decode(encoded)
	image = Image.open(io.BytesIO(decoded))
	processed_image = preprocess_image(image, target_size=(64, 64))
	
	prediction = model.predict(processed_image).tolist()
	
	response = {
		'prediction': {
			'original': prediction[0][0],
			'filtered': prediction[0][1]
		}
	}
	
	print(response)
	
	
	return jsonify(response)

@app.route("/store",methods=["POST"])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])

def store():
	print("In store function")
	userInfo = request.get_json(force=True)
	age = userInfo['age']
	location = userInfo['location']
	education = userInfo['education']
	gender=userInfo['gender']
	pred1 = userInfo['pred1']
	pred2 = userInfo['pred2']
	pred3 = userInfo['pred3']
	pred4 = userInfo['pred4']
    
	print(age)
	print(location)
	print(education)
	print(gender)
	print(pred1)
	print(pred2)
	print(pred3)
	print(pred4)

	return render_template('thankyou.html')
	# response = "thank you"
	# return jsonify(response)

if __name__ == "__main__":
	app.run()
