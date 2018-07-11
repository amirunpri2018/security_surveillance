import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import cv2
import re
import os
import requests

cap = cv2.VideoCapture(0)
ret, img = cap.read()

url = 'http://192.168.0.102:8000/predict/'
#url = 'http://13.126.171.131:8000/predict/'

while not(ret):  # my sexy logic to wait till the camera is ready
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    print('Restarting the camera...')
    time.sleep(1)
    
print('Camera has been started!')

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global cameraQuality
        try:
            self.path=re.sub('[^.a-zA-Z0-9]', "",str(self.path))
            if self.path=="" or self.path==None or self.path[:1]==".":
                return
            
            if self.path.endswith(".mjpeg"):
                self.send_response(200)
                self.wfile.write("Content-Type: multipart/x-mixed-replace; boundary=--aaboundary")
                self.wfile.write("\r\n\r\n")
                while True:
                    ret, img = cap.read()
                    cv2mat = cv2.imencode('.jpg', img, (cv2.IMWRITE_JPEG_QUALITY,20))  # low quality video streaming
                    JpegData = cv2mat[1].tostring()
                    self.wfile.write("--aaboundary\r\n")
                    self.wfile.write("Content-Type: image/jpeg\r\n")
                    self.wfile.write("Content-length: "+str(len(JpegData))+"\r\n\r\n" )
                    self.wfile.write(JpegData)
                    self.wfile.write("\r\n\r\n\r\n")
                    time.sleep(0.05)
                return

            if self.path.endswith(".jpg"):
                ret, frame = cap.read()
                cv2.imwrite('/home/pi/Desktop/security_serveillance/raspberry_pi/object_detection/frame.jpg', frame)                
                self.send_response(200)
                time.sleep(0.05)
                return

            if self.path.endswith(".clip"):
                print ('In Video Recorder')
                
                # video recorder
                fourcc = cv2.cv.CV_FOURCC(*'XVID')
                videoOut = cv2.VideoWriter("/home/pi/Desktop/security_serveillance/raspberry_pi/object_detection/video_clip.avi",
                                           fourcc, 20.0,(640, 480))              
                start_time = time.time()
                frame_count = 0
                frame_list = []
                while True:
                    ret, frame = cap.read()
                    frame_count += 1
                    
                    print('Time:',int(time.time()-start_time), 'sec')
                    frame_list.append(frame)
                    if int(time.time()-start_time) == 15:                        
                        break 
                        # get out of loop after 15 sec video                  
                
                for f in frame_list:
                    videoOut.write(f)  # write each frame to make video clip
    
                time.sleep(0.5) 
                videoOut.release()

                object_name = []
                object_score = []
            
                with open('/home/pi/Desktop/security_serveillance/raspberry_pi/object_detection/video_url.txt', 'r') as f:
                    s = f.read()
                # Get the latest localtunnel url from saved in file
                vid_url = s.split('\n')[-2]
                video_url = vid_url[13:]+"/something.mjpeg"  # make it as video streaming url

                object_name.append('video_url')
                object_score.append(video_url)
                object_name.append('message')
                object_score.append('video')

                detected_objects = dict(zip(object_name, object_score))
                files = {'video': open('/home/pi/Desktop/security_serveillance/raspberry_pi/object_detection/video_clip.avi', 'rb')}                              
                try:
                    response = requests.post(url, files=files, data=detected_objects)
                    print('Video Uploaded!')
                except:
                    print('Video upload failed!')
                
                os.remove('/home/pi/Desktop/security_serveillance/raspberry_pi/object_detection/video_clip.avi')
                self.send_response(200)                
                return
            return 
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():
    try:
        server = ThreadedHTTPServer(('localhost', 8080), MyHandler)
        print ('HTTP Server started...')
        server.serve_forever()
    except KeyboardInterrupt:
        print ('Shutting down the Webcam Server...')
        server.socket.close()

if __name__ == '__main__':
    main()

