"""
Project Start Date: 11/16/21
"""

#Load Libs
import os
import cv2
import sys
import time
import numpy
from tkinter import *
from tkinter import filedialog

#Dir fix
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Global Vars
ver = "0.0.5"
camport = 'null'

p = open('persistent.capt', 'r')
per = p.readlines()
point1R = per[1]
point1G = per[2]
point1B = per[3]
point1S = per[4]
point2R = per[6]
point2G = per[7]
point2B = per[8]
point2S = per[9]
point3R = per[11]
point3G = per[12]
point3B = per[13]
point3S = per[14]
point4R = per[16]
point4G = per[17]
point4B = per[18]
point4S = per[19]

#Clean newline
point1R = point1R[:-1]
point1G = point1G[:-1]
point1B = point1G[:-1]
point1S = point1S[:-1]
point2R = point2R[:-1]
point2G = point2G[:-1]
point2B = point2B[:-1]
point2S = point2S[:-1]
point3R = point3R[:-1]
point3G = point3G[:-1]
point3B = point3B[:-1]
point3S = point3S[:-1]
point4R = point4R[:-1]
point4G = point4G[:-1]
point4B = point4B[:-1]
point4S = point4S[:-1]

#Debug Colors
class eventcolors:
    WARNING = '\033[91mWarning: '
    DEBUG = '\033[90mDebug: '
    PASS = '\033[92mInfo: '
    ENDC = '\033[0m'
    
#Functions
def CollectRGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSECLICK:  # checks mouse moves
        colorsBGR = image[y, x]
        colorsRGB=tuple(reversed(colorsBGR)) #Reversing the OpenCV BGR format to RGB format
        print("RGB Value at ({},{}):{} ".format(x,y,colorsRGB))
    
#INIT Message
print(f"{eventcolors.DEBUG}Starting CAPTv" + ver + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Current Dir: "+ os.getcwd() + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Colors1 Per " + point1R + ',' + point1G + ',' + point1B + ',' + point1S + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Colors2 Per " + point2R + ',' + point2G + ',' + point2B + ',' + point2S + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Colors3 Per " + point3R + ',' + point3G + ',' + point3B + ',' + point3S + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Colors4 Per " + point4R + ',' + point4G + ',' + point4B + ',' + point4S + f"{eventcolors.ENDC}")

#Find Cam Port
cap = cv2.VideoCapture(0)
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(1)
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(2)
        if cap is None or not cap.isOpened():
            print(f"{eventcolors.WARNING}Can't find a camera pluged in{eventcolors.ENDC}")
            print(f"{eventcolors.DEBUG}Check if your device is pluged into the device all the way{eventcolors.ENDC}")
            time.sleep(3)
            sys.exit()
        else:
            print(f"{eventcolors.PASS}Cam found on port 2{eventcolors.ENDC}")
            camport = 2
    else:
        print(f"{eventcolors.PASS}Cam found on port 1{eventcolors.ENDC}")
        camport = 1
else:
    print(f"{eventcolors.PASS}Cam found on port 0{eventcolors.ENDC}")
    camport = 0
    
#Frame Setup
cv2.namedWindow('Capture From Port ' + str(camport))
cv2.setMouseCallback('Capture From Port ' + str(camport), CollectRGB)

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
        print(f"{eventcolors.DEBUG}Terminating {eventcolors.ENDC}")
        sys.exit()
