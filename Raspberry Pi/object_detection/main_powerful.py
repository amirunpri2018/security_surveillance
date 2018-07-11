import requests
url = 'http://13.126.171.131:8000/predict/'
import detect_object
response = requests.post(url, data={'detected_faces':'tensorflow'})
print('tensorflow ready')
import cv2        # To capture the images/video from the security camera
import requests   # To send the snapshot and detected objects to the server
import time
import os
import sys
import threading
#import face_recognition
#response = requests.post(url, data={'detected_faces':'face_detection'})
# server url to post the snapshot and detected object

once_upload = False

cap = cv2.VideoCapture(0)
def server_upload(object_name, object_score):
    detected_objects = dict(zip(object_name, object_score))
    files = {'media': open('/home/pi/Desktop/security_serveillance/raspberry_pi/object_detection/frame.jpg', 'rb')}
    try:
        response = requests.post(url, files=files, data=detected_objects)
        print('Data has been uploaded on Server!')
    except:
        print('Failed to upload on Server!')


snapshot_path = "/home/pi/Desktop/security_serveillance/raspberry_pi/object_detection/frame.jpg"  # snapshot of camera frame


    
ret, image = cap.read()
if ret == False:
    time.sleep(5)
    print('Restarting the camera...')
    cap = cv2.VideoCapture(0)
else:
    response = requests.post(url, data={'detected_faces':'camera'})
    print('Camera has been started!')
    
response = requests.post(url, data={'detected_faces':'ready'})

def knife_thread():
    knife_confidence = detect_object.knife(snapshot_path)
    if knife_confidence > 0.60:
        global_object_name.append('knife')
        global_object_score.append(str(knife_confidence)[:5])
    global_object_name.append('detected_faces')
    global_object_score.append('face detection is off')
    
def general_thread():
    object_name, object_score = detect_object.general(snapshot_path)
    global_object_name.extend(object_name)
    global_object_score.extend(object_score)




while True:
    global_object_name = []
    global_object_score = []
    ret, image = cap.read()
    cv2.imwrite('/home/pi/Desktop/security_serveillance/raspberry_pi/object_detection/frame.jpg', image)
    model_start = time.time()
    thread1 = threading.Thread(target=knife_thread)
    thread2 = threading.Thread(target=general_thread)
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    print('model took', time.time()-model_start)    
    print(global_object_name, global_object_score)
    if (('person' in global_object_name) or ('knife' in global_object_name)): 
        server_upload(global_object_name, global_object_score)
        once_upload = True
    else:
        if once_upload:
            object_name = ['detected_faces']
            object_score = ['abort']
            # send empty data to clear the dashboard
            server_upload(object_name, object_score)
            once_upload = False
        print('Not uploading any data!')
