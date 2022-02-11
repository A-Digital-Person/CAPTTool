"""
Project Ver: 0.0.2
Project Start Date: 11/16/21
Project Last Edit: 11/17/21
Project Last Ver Change: 11/16/21
"""

#Load Libs
import cv2
import sys
import time

#Global Vars
ver = "0.0.1"
camport = 'null'

#Debug Colors
class eventcolors:
    WARNING = '\033[91m'
    DEBUG = '\033[90m'
    PASS = '\033[92m'
    BG = '\033[100m'
    ENDC = '\033[0m'
    
#INIT Message
print(f"{eventcolors.DEBUG}Debug: Starting {eventcolors.ENDC}")

#Find Cam Port
cap = cv2.VideoCapture(0)
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(1)
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(2)
        if cap is None or not cap.isOpened():
            print(f"{eventcolors.WARNING}Warning: Can't find a camera pluged in{eventcolors.ENDC}")
            print(f"{eventcolors.DEBUG}Debug: Check if your device is pluged into the device all the way{eventcolors.ENDC}")
            time.sleep(3)
            sys.exit()
        else:
            print(f"{eventcolors.PASS}{eventcolors.BG}Pass: Cam found on port 2{eventcolors.ENDC}")
            camport = 2
    else:
        print(f"{eventcolors.PASS}{eventcolors.BG}Pass: Cam found on port 1{eventcolors.ENDC}")
        camport = 1
else:
    print(f"{eventcolors.PASS}{eventcolors.BG}Pass: Cam found on port 0{eventcolors.ENDC}")
    camport = 0
    
#Frame Setup
cv2.namedWindow('Capture From Port ' + str(camport))

#Capture Image
cap = cv2.VideoCapture(camport)

#Quit Event
while True:
    keypressed = cv2.waitKey(1)
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imshow('Capture From Port ' + str(camport), frame)
    if keypressed == 27:
        cap.release()
        cv2.destroyAllWindows()
        print(f"{eventcolors.DEBUG}Debug: Terminating {eventcolors.ENDC}")
        sys.exit()
