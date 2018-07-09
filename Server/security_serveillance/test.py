##import requests
##
##on = []
##os = []
##
##url = 'http://127.0.0.1:8000/predict/'
# on.append('video_url')
# os.append('xyz')
##
# on.append('message')
# os.append('video')
##
##do = dict(zip(on, os))
##
##f = {'snapshot': open('test.avi', 'rb')}
##
# try:
##    r = requests.post(url, files=f, data=do, timeout=3)
# except:
# print 'to'
# print 'img sent'
##
##import subprocess as s
import os
####dv = s.call("ffmpeg -i test.avi -c:v libx264 -crf 23 -c:a libfaac -q:a 100 output.mp4", shell=True)
##os.system("ffmpeg -i test.avi win2.mp4")
# rint 'done'
p = "C:\\Users\\Prasad\\Desktop\\Security and Serveillance\\Server\\manage.py"
file_path = os.path.relpath(p)
print file_path
os.system("ffmpeg -i video_clip.avi video_clip.mp4 -y")
print 'done'
