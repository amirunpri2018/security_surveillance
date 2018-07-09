# Security and Serveillance System
Security and Serveillance system using Tensorflow Object Detection API and Opencv

 <p align="center">
  <img src="home_page_new.jpg" width=800 height=450>
 </p> 
 
 When we click on "know more about people" link it will give a big list of detected faces of people:
 <p align="center">
  <img src="more_about_people.jpg" width=800 height=250>
 </p> 
 
 You can search for required person:
 <p align="center">
  <img src="search_people.jpg" width=800 height=230>
 </p> 
 <hr>

## Installations and Setup:
```bash
# Download Tensorflow 1.4.0 on RPi for Python3
wget http://ci.tensorflow.org/view/Nightly/job/nightly-pi-python3/39/artifact/output-artifacts/tensorflow-1.4.0-cp34-none-any.whl
sudo pip3 install ./tensorflow-1.4.0-cp34-none-any.whl

# Verify the Installation:
python3
>> import tensorflow as tf
>> tf.VERSION

# Install matplotlib on RPi for Python3
sudo pip3 install matplotlib
sudo apt-get install python3-cairo

# Auto start python script when RPi boots:
sudo apt-get install daemontools daemontools-run
crontab -e
@reboot sudo python /home/pi/Desktop/test.py /home/pi/Desktop/log.txt

# Another method for auto execution of python script in rpi:
1. Make a directory in /home/.config/ named as autostart
2. Create a file xyz.desktop and paste the following content:

[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=ss_app
Comment=
Exec=python3 /path/to/python/script.py
StartupNotify=false
Terminal=true
Hidden=false

```
Install Opencv3 on RPi for Python3

Youtube Video: 
https://www.youtube.com/watch?v=ZuhPzP5lt9U&t=1099s

Blog:
http://www.life2coding.com/install-opencv-3-4-0-python-3-raspberry-pi-3/

```bash
# Install Python2 64-bit on EC2 Windows
pip install django
pip install django-rest_framework
pip install requests
pip install bs4
pip install Pillow
pip install django-cors-headers
```


