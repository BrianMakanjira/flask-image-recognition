from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
import tensorflow as tf
import os
import cv2

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
    output_dir = os.path.join('frames', os.path.splitext(filename)[0])
    print(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Read and save each frame from the video file
    frame_count = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        cv2.imwrite(os.path.join(output_dir, f'frame_{frame_count}.jpg'), frame)
        frame_count += 1
    
    # Release the video file
    cap.release()