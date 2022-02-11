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
ver = "0.0.6"
camport = 'null'
cal = 0
maxsen = 20

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
    CLB = '\033[95mCalibration: '
    ENDC = '\033[0m'
    
#Functions
def CollectRGB(event, x, y, flags, param):
    global cal
    if event == cv2.EVENT_LBUTTONDOWN:  # checks mouse moves
        colorsBGR = frame[y, x]
        colorsRGB=tuple(reversed(colorsBGR)) #Reversing the OpenCV BGR format to RGB format
        if cal == 1:
            point1R = colorsRGB[0]
            point1G = colorsRGB[1]
            point1B = colorsRGB[2]
            print(f"{eventcolors.CLB}Setting Colors For Point 1{eventcolors.ENDC}")
            cal = 0
        if cal == 2:
            point1R = colorsRGB[0]
            point1G = colorsRGB[1]
            point1B = colorsRGB[2]
            print(f"{eventcolors.CLB}Setting Colors For Point 2{eventcolors.ENDC}")
            cal = 0
        if cal == 3:
            point1R = colorsRGB[0]
            point1G = colorsRGB[1]
            point1B = colorsRGB[2]
            print(f"{eventcolors.CLB}Setting Colors For Point 3{eventcolors.ENDC}")
            cal = 0
        if cal == 4:
            point1R = colorsRGB[0]
            point1G = colorsRGB[1]
            point1B = colorsRGB[2]
            print(f"{eventcolors.CLB}Setting Colors For Point 4{eventcolors.ENDC}")
            cal = 0
        if cal == 0:
            print(f"{eventcolors.CLB}Red: " + str(colorsRGB[0]) + f"{eventcolors.ENDC}")
            print(f"{eventcolors.CLB}Green: " + str(colorsRGB[1]) + f"{eventcolors.ENDC}")
            print(f"{eventcolors.CLB}Blue: " + str(colorsRGB[2]) + f"{eventcolors.ENDC}")
    
#INIT Message
print(f"{eventcolors.DEBUG}Starting CAPTv" + ver + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Current Dir: "+ os.getcwd() + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Color 1 Per " + point1R + ',' + point1G + ',' + point1B + ',' + point1S + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Color 2 Per " + point2R + ',' + point2G + ',' + point2B + ',' + point2S + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Color 3 Per " + point3R + ',' + point3G + ',' + point3B + ',' + point3S + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Color 4 Per " + point4R + ',' + point4G + ',' + point4B + ',' + point4S + f"{eventcolors.ENDC}")

point1R = int(point1R)
point1G = int(point1G)
point1B = int(point1G)
point1S = int(point1S)
point2R = int(point2R)
point2G = int(point2G)
point2B = int(point2B)
point2S = int(point2S)
point3R = int(point3R)
point3G = int(point3G)
point3B = int(point3B)
point3S = int(point3S)
point4R = int(point4R)
point4G = int(point4G)
point4B = int(point4B)
point4S = int(point4S)

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
cv2.namedWindow('Filitered')
cv2.setMouseCallback('Capture From Port ' + str(camport), CollectRGB)

cv2.namedWindow("Sensitivity")
cv2.createTrackbar('Point1','Sensitivity',int(point1S),maxsen,lambda x:None)
cv2.createTrackbar('Point2','Sensitivity',int(point2S),maxsen,lambda x:None)
cv2.createTrackbar('Point3','Sensitivity',int(point3S),maxsen,lambda x:None)
cv2.createTrackbar('Point4','Sensitivity',int(point4S),maxsen,lambda x:None)


#Capture Image
cap = cv2.VideoCapture(camport)
ftimg = ''
def maskit():
    global ftimg
    global point1R
    global point1G
    global point1B
    global point1S
    global point2R
    global point2G
    global point2B
    global point2S
    global point3R
    global point3G
    global point3B
    global point3S
    global point4R
    global point4G
    global point4B
    global point4S
    point1min = [point1R,point1G,point1B]
    point1max = [point1R+point1S,point1G+point1S,point1B+point1S]
    point2min = [point2R,point2G,point2B]
    point2max = [point2R+point2S,point2G+point2S,point1B+point2S]
    point3min = [point3R,point3G,point3B]
    point3max = [point3R+point3S,point3G+point3S,point1B+point3S]
    point4min = [point4R,point4G,point4B]
    point4max = [point4R+point4S,point4G+point4S,point1B+point4S]
    
    #print (point1min, point1max)
    
    point1min = numpy.array(point1min, dtype = "uint8")
    point1max = numpy.array(point1max, dtype = "uint8")
    point2min = numpy.array(point2min, dtype = "uint8")
    point2max = numpy.array(point2max, dtype = "uint8")
    point3min = numpy.array(point3min, dtype = "uint8")
    point3max = numpy.array(point3max, dtype = "uint8")
    point4min = numpy.array(point4min, dtype = "uint8")
    point4max = numpy.array(point4max, dtype = "uint8")
    
    block1 = cv2.inRange(frame,point1min,point1max)
    block2 = cv2.inRange(frame,point2min,point2max)
    block3 = cv2.inRange(frame,point3min,point3max)
    block4 = cv2.inRange(frame,point4min,point4max)
    
    f1 = cv2.bitwise_or(frame, frame, mask=block1)
    f2 = cv2.bitwise_or(frame, frame, mask=block2)
    f3 = cv2.bitwise_or(frame, frame, mask=block3)
    f4 = cv2.bitwise_or(frame, frame, mask=block4)
    
    final = cv2.bitwise_or(f1, f2)
    final = cv2.bitwise_or(final, f3)
    ftimg = cv2.bitwise_or(final, f4)
        
#Quit Event
while True:
    keypressed = cv2.waitKey(1)
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if cal == 0:
        maskit()
    cv2.imshow('Capture From Port ' + str(camport), frame)
    cv2.imshow('Filitered', ftimg)
    if keypressed == 27:
        cap.release()
        cv2.destroyAllWindows()
        print(f"{eventcolors.DEBUG}Terminating {eventcolors.ENDC}")
        sys.exit()
    elif keypressed == ord('1'):
        cal = 1
        print(f"{eventcolors.DEBUG}Calbrate Point 1{eventcolors.ENDC}")
    elif keypressed == ord('2'):
        cal = 2
        print(f"{eventcolors.DEBUG}Calbrate Point 2{eventcolors.ENDC}")
    elif keypressed == ord('3'):
        cal = 3
        print(f"{eventcolors.DEBUG}Calbrate Point 3{eventcolors.ENDC}")
    elif keypressed == ord('4'):
        cal = 4
        print(f"{eventcolors.DEBUG}Calbrate Point 4{eventcolors.ENDC}")
