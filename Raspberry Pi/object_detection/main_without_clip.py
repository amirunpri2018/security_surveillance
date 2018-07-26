import requests  # To send the snapshot and detected objects to the server
import time

#url = 'http://13.126.171.131:8000/predict/'
#url = 'http://192.168.0.102:8000/predict/'
url = 'http://127.0.0.1:8000/predict/'

response = requests.post(url, data={'message': 'Setting up!'})

import detect_object  # Intialize the object detection graph
response = requests.post(url, data={'message': 'Tensorflow Ready!'})

import os
import sys

once_upload = False


def server_upload(object_name, object_score):
    detected_objects = dict(zip(object_name, object_score))
    files = {'snapshot': open('frame.jpg', 'rb')}
    try:
        response = requests.post(
            url, files=files, data=detected_objects, timeout=3)
        print('Data has been uploaded on Server!')
    except:
        print('Failed to upload on Server!')


snapshot_path = "frame.jpg"
# snapshot of camera frame to detect objects

response = requests.post(url, data={'message': 'ready'})

time.sleep(1)  # Take a breath, Let's go

while True:
    with open('video_url.txt', 'r') as f:
        s = f.read()
    # Get the latest localtunnel url from saved in file
    vid_url = s.split('\n')[-2]
    # make it as video streaming url
    video_url = vid_url[13:]+"/something.mjpeg"

    r = requests.get('http://127.0.0.1:8080/snapshot.jpg')
    # save the image

    # initialize variables to store detected objects and score
    object_name = []
    object_score = []

    model_start = time.time()
    detected_obj, detected_score = detect_object.general(snapshot_path)
    print('Model took', time.time()-model_start, 'to detect the objects.')

    object_name.extend(detected_obj)
    object_score.extend(detected_score)
    object_name.append('video_url')
    object_score.append(video_url)
    object_name.append('message')
    object_score.append('snapshot')

    print('Detection List:', object_name, object_score)

    if ('person' in object_name):  # If person is detected
        server_upload(object_name, object_score)
        once_upload = True  # to stop continuous uploading of blank data on server
    else:
        if once_upload:
            object_score.remove('snapshot')
            object_score.append('abort')
            detected_objects = dict(zip(object_name, object_score))
            # send abort message with 'video_url' key to clear the dashboard
            try:
                response = requests.post(url, data=detected_objects, timeout=3)
                once_upload = False
            except:
                print('Error occured in once upload')
        print('Not uploading any data!')
