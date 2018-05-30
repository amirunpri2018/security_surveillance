import cv2
import numpy as np
import sqlite3     # for database operations

face_detect = cv2.CascadeClassifier(
    'face_recognition_model/haarcascade_frontalface_default.xml')
# load pre-trained face detection classifier

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_recognition_model/rpi_training_data.yml')
# above is for rpi cv2 version 3.4

# following is for cv2 version 2.4
# recognizer = cv2.createLBPHFaceRecognizer()
# recognizer.load('recognizer/training_data.yml')



recognizer.read('face_recognition_model/rpi_training_data.yml')

def detect_face(image_path):
    frame = cv2.imread(image_path)
    detected_faces = []   # list of names of the detected faces
    grayscaled_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Need to convert into grayscaled to detect faces

    faces = face_detect.detectMultiScale(grayscaled_image, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # frame = image on which we are going to draw a rectangle
        # (x, y) = coordinates of the face
        # (x + w, y + h) = Height and Width
        # Green Color
        # width of the rectangle = 2px

        id_, confidence = recognizer.predict(
            grayscaled_image[y:y + h, x:x + w])
        # here confidence is relatively opposite
        # means lesser the value, more will be the accuracy
        
        if id_ == 1 and confidence < 55:
            detected_faces.append('Prasad')

        if id_ == 2 and confidence < 55:
            detected_faces.append('Hrushikesh')

        if id_ == 3 and confidence < 55:
            detected_faces.append('Sakshi')

        if confidence > 80:
            detected_faces.append('Unknown')

    return detected_faces
