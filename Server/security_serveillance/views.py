# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Snapshots, AlertChoice
import json
import sms_alert  # Import this module to send text messages

mobile_number = '8983050329'
# Mobile number to which the alert message will be sent


def page_load(request):  # http://127.0.0.1:8000/lmtech/
    if request.method == 'GET':
        global analysis  # Declare a global list var to use it in get function
        analysis = []    # Declare an empty list to send response
        # Here, analysis list is declared because if RPi is not posting any
        # data then there will not be any variable 'analysis in get request

        try:
            # Get the status of all alerts from the database
            latest_alert_status = AlertChoice.objects.latest('id').alert_status
            status_list = latest_alert_status.split(',')
            # Make a list of those string formatted alert status

            object_list = ['Person', 'Knife',
                           'Handbag', 'Bottle', 'Dog', 'Cat']

            # Make a dict of object and its alert-status
            alert_states = dict(zip(map(str, object_list), map(str,
                                                               status_list)))
            context = {
                "alert_states": json.dumps(alert_states),
            }
        except:
            print('Setting initia values for the alerts to false')
            status_list = ['true', 'false', 'false', 'false', 'false', 'false']
            alert_states = dict(zip(map(str, object_list), map(str, status_list)))

            context = {
                "alert_states": json.dumps(alert_states),
            }
        return render(request, "home_page.html", context)


class PredictImageObject(APIView):    # http://127.0.0.1:8000/predict/

    def alert(self, detected_object):
        try:
            message = sms_alert.sms()
            message.send(mobile_number,
                         detected_object + ' has been detected!')
            sent_count = message.msgSentToday()
            print 'Message Sent Count =', sent_count
            message.logout()
        except:
            print 'Message sending Failed!'

    def check_alerts(self, predicted_objects, confidence):
        # Get the latest status of activated alerts from the database
        latest_alert_status = AlertChoice.objects.latest('id').alert_status
        status_list = latest_alert_status.split(',')
        # Make a list of those string formatted alert status

        # Check if the object is detected and alert for that object is ON
        # Call alert method to send text message
        if ('person' in predicted_objects) and status_list[0] == 'true':
            self.alert('Person')
        if ('knife' in predicted_objects) and status_list[1] == 'true':
            self.alert('Knife')
        if ('handbag' in predicted_objects) and status_list[2] == 'true':
            self.alert('Handbag')
        if ('bottle' in predicted_objects) and status_list[3] == 'true':
            self.alert('Bottle')
        if ('dog' in predicted_objects) and status_list[4] == 'true':
            self.alert('Dog')
        if ('cat' in predicted_objects) and status_list[5] == 'true':
            self.alert('Cat')

    def post(self, request):  # RPi will post the detected objects on this url
        global predicted_objects  # Holds the list of detected objects
        predicted_objects = []

        global confidence  # Holds the list of probability of detected objects
        confidence = []

        global analysis  # Declare a global list var to use it in get function
        analysis = []    # Declare an empty list to send response
        print 'request data:', request.data
        media_file = Snapshots(picture=request.FILES['media'], detected_faces=request.data['detected_faces'])
        media_file.save()  # Save the snapshot in database
        # Get the saved latest snapshot image name and path
        file_path = Snapshots.objects.latest('id').picture

        try:
            for key, value in request.data.items():
                if key == 'media' or key == 'tv' or key == 'detected_faces':
                    continue
                    # do not add snapshot in objects list just go ahead
                else:
                    # add detected objects and their probabilities in list
                    predicted_objects.append(key)
                    confidence.append(value)
                    # Dict(json object) to give at frontend in get method
                    analysis.append({
                        'label': key,   
                        'confidence': str(value)[:5],
                        'file_path': str(file_path)
                    })

            # Logic to remove previous data from the table
            while len(analysis) < 7:
                analysis.append({
                    'label': '',
                    'confidence': '',
                    'file_path': str(file_path)
                })
            # print "Detected objects:", analysis
            self.check_alerts(predicted_objects, confidence)
        except:
            print 'Failed to get the detected objects!'
        return Response("Success!")

    def get(self, request):  # This will get the alert status and response with object detection analysis
        alert_status_string = request.GET.get('alert')
        try:
            # Save the selected alerts only if there is change in status
            # Get the existing status of alert choices
            latest_alert_status = AlertChoice.objects.latest('id').alert_status
        except:  # If there is no alert status in database
            print 'No alerts were saved in database'
            latest_alert_status = 0  # Flag that there were no alert status
        if latest_alert_status == 0 or \
                (latest_alert_status != alert_status_string):
            # User has changed the status of alerts
            # Therefore save the alert status in Database
            alert_update = AlertChoice(alert_status=alert_status_string)
            alert_update.save(force_insert=True)
            print 'Database updated with current alert status!'
        return Response(analysis)
