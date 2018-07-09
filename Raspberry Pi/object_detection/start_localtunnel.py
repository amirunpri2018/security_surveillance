import subprocess
import time
import requests

time.sleep(1)
#url = 'http://13.126.171.131:8000/predict/'
#r = requests.post(url, {'detected_faces': 'tunnel is ready to fetch the video'})

while True:
    subprocess.call("sh /home/pi/Desktop/security_serveillance/raspberry_pi/object_detection/start_localtunnel.sh", shell=True)
    print('Restarting the tunnel')


