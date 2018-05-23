import detect_object
import cv2        # To capture the images/video from the security camera
import requests   # To send the snapshot and detected objects to the server
import time
import threading  # To do multiple task
import os
import sys


import face_recognition

print('Module imports Successful!')
url = 'http://192.168.0.101:8000/predict/'
# server url to post the snapshot and detected object
cap = cv2.VideoCapture(0)
print('Starting the camera!')

def server_upload(object_name, object_score):
    detected_objects = dict(zip(object_name, object_score))
    files = {'media': open('frame.jpg', 'rb')}
    try:
        response = requests.post(url, files=files, data=detected_objects)
        print('Data has been uploaded on Server!')
    except:
        print('Failed to upload on Server!')


snapshot_path = "frame.jpg"  # snapshot of camera frame

ret, image = cap.read()
if ret == False:
    time.sleep(5)
    print('Restarting the camera...')
    cap = cv2.VideoCapture(0)
else:
    print('Camera has been started!')
    

while True:
    ret, image = cap.read()
    cv2.imwrite('frame.jpg', image)
    time.sleep(0.2)
    knife_confidence = detect_object.knife(snapshot_path)
    object_name, object_score = detect_object.general(snapshot_path)
    detected_faces = face_recognition.detect_face(snapshot_path)

    if len(detected_faces) > 1:  # if more than one faces detected
        faces_string = ','.join(detected_faces)    
    elif detected_faces:
        face_string = detected_faces[0]
    else:
        face_string = 'No face detected!'
        
    if knife_confidence > 0.60:
        object_name.append('knife')
        object_score.append(str(knife_confidence)[:5])

    object_name.append('detected_faces')
    object_score.append(face_string)
    server_upload(object_name, object_score)
    print(object_name, object_score)
