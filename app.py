# Importing required libraries
from flask import Flask, render_template, request, jsonify, send_from_directory
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions, InceptionV3
from tensorflow.keras.models import load_model
import os
import tensorflow as tf
import cv2
import random


# Instantiating flask app
app = Flask(__name__)

# Load the pre-trained Inception V3 model
# model = load_model('model.h5')
model = InceptionV3(weights='imagenet',include_top=True)

#defining a function that generates frames from a video
def generateFrames():
    # check if the post request has the file part
    if ('file' not in request.files):
        return jsonify({'error': 'No valid file uploaded'})
    # if a file has been uploaded
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without filename
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    # creating an uploads folder if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Save the file to the uploads folder
    filename = file.filename
    file.save(os.path.join('uploads', filename))
    # Open the video file
    cap = cv2.VideoCapture(os.path.join('uploads', filename))
    
    # Check if the video file was opened successfully
    if not cap.isOpened():
        return jsonify({'error': 'Failed to open video file'})
    
    # Create a directory to store the frames
    if not os.path.exists('frames'):
        os.makedirs('frames')

    # Read and save each frame from the video file
    frame_count = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        cv2.imwrite(os.path.join('frames', f'frame_{frame_count}.jpg'), frame)
        frame_count += 1
    
    # Release the video file
    cap.release()

# processing the frames
def predict(image_file):
    img = image.load_img(image_file, color_mode='rgb', target_size=(299,299))
    img = image.img_to_array(img)
    img_arr = np.expand_dims(img, axis=0)
    img_arr = preprocess_input(img_arr)
    predictions = model.predict(img_arr)
    return decode_predictions(predictions)

# Home route
@app.route("/")
def main():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def process_video():
    # generating the frames
    generateFrames()

    # mapping through the images in the frames directory and making predictions
    predictions = []

    randomlist = random.sample(range(1,len(os.listdir('frames'))), 50)
    random.sample(range(1, 100), 3)

    for i in randomlist:
        name = f'frame_{i}.jpg'
        pred = predict(os.path.join('frames',name))
        for item in pred[0]:
            predictions.append({ 'name': name, 'prediction': item[1]})

    # # removing duplicates
    # predictions = list(set(predictions))
    
    return render_template("result.html", predictions=predictions)
    
@app.route('/frames/<filename>')
def serve_image(filename):
    root_dir = os.getcwd()
    return send_from_directory('frames', filename)


if __name__ == "__main__":
    app.run(port=5000, debug=True)