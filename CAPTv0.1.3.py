import cv2
import numpy
import os
import sys

ver = "0.1.2"

class eventcolors:
    WARNING = '\033[91mWarning: '
    DEBUG = '\033[90mDebug: '
    PASS = '\033[92mInfo: '
    CLB = '\033[95mCalibration: '
    ENDC = '\033[0m'
    
print(f"{eventcolors.DEBUG}Starting CAPTv" + ver + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Current Dir: "+ os.getcwd() + f"{eventcolors.ENDC}")

def savesession():
    print ('My application is ending!')

if os.path.exists(os.getcwd() + 'persistent.capt'):
    print(f"{eventcolors.DEBUG}Using last session{eventcolors.ENDC}")
else:
    print(f"{eventcolors.DEBUG}No session found. Creating new...{eventcolors.ENDC}")
    p = open('persistent.capt', 'w')
    p.write("Color1HSV\n0\n0\n0\n0\n0\n0\nColor2\n0\n0\n0\n0\n0\n0\nColor3\n0\n0\n0\n0\n0\n0\nColor4\n0\n0\n0\n0\n0\n0\n")
    p.close()
    
p = open('persistent.capt', 'r')
per = p.readlines()
H1 = per[1]
S1 = per[2]
V1 = per[3]

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

cv2.namedWindow("Orginal")
cv2.namedWindow("Mask")
cv2.namedWindow("CTRL1")
cv2.namedWindow("CTRL2")
cv2.namedWindow("CTRL3")
cv2.namedWindow("CTRL4")

cv2.resizeWindow("CTRL1", 300, 300)
cv2.resizeWindow("CTRL2", 300, 300)
cv2.resizeWindow("CTRL3", 300, 300)
cv2.resizeWindow("CTRL4", 300, 300)

hhigh = 255
shigh = 255
vhigh = 255

cv2.createTrackbar("H Min", "CTRL1", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL1", 0, shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL1", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL1", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL1", 0, shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL1", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL2", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL2", 0, shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL2", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL2", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL2", 0, shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL2", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL3", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL3", 0, shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL3", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL3", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL3", 0, shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL3", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL4", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL4", 0, shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL4", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL4", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL4", 0, shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL4", 0, vhigh, lambda x:None)

keypress = 1

while (keypress != 27):
    ret, frame = cap.read()
    
    hsvframe = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    c1vl = cv2.getTrackbarPos("V Min", "CTRL1")
    c1sl = cv2.getTrackbarPos("S Min", "CTRL1")
    c1hl = cv2.getTrackbarPos("H Min", "CTRL1")
    c1vh = cv2.getTrackbarPos("V Max", "CTRL1")
    c1sh = cv2.getTrackbarPos("S Max", "CTRL1")
    c1hh = cv2.getTrackbarPos("H Max", "CTRL1")
    
    c2vl = cv2.getTrackbarPos("V Min", "CTRL2")
    c2sl = cv2.getTrackbarPos("S Min", "CTRL2")
    c2hl = cv2.getTrackbarPos("H Min", "CTRL2")
    c2vh = cv2.getTrackbarPos("V Max", "CTRL2")
    c2sh = cv2.getTrackbarPos("S Max", "CTRL2")
    c2hh = cv2.getTrackbarPos("H Max", "CTRL2")
    
    c3vl = cv2.getTrackbarPos("V Min", "CTRL3")
    c3sl = cv2.getTrackbarPos("S Min", "CTRL3")
    c3hl = cv2.getTrackbarPos("H Min", "CTRL3")
    c3vh = cv2.getTrackbarPos("V Max", "CTRL3")
    c3sh = cv2.getTrackbarPos("S Max", "CTRL3")
    c3hh = cv2.getTrackbarPos("H Max", "CTRL3")
    
    c4vl = cv2.getTrackbarPos("V Min", "CTRL4")
    c4sl = cv2.getTrackbarPos("S Min", "CTRL4")
    c4hl = cv2.getTrackbarPos("H Min", "CTRL4")
    c4vh = cv2.getTrackbarPos("V Max", "CTRL4")
    c4sh = cv2.getTrackbarPos("S Max", "CTRL4")
    c4hh = cv2.getTrackbarPos("H Max", "CTRL4")
    
    c1l = [c1hl,c1sl,c1vl]
    c1h = [c1hh,c1sh,c1vh]
    
    c2l = [c2hl,c2sl,c2vl]
    c2h = [c2hh,c2sh,c2vh]

    c3l = [c3hl,c3sl,c3vl]
    c3h = [c3hh,c3sh,c3vh]
    
    c4l = [c4hl,c4sl,c4vl]
    c4h = [c4hh,c4sh,c4vh]
    
    c1l = numpy.array(c1l, dtype = "uint8")
    c1h = numpy.array(c1h, dtype = "uint8")
    c2l = numpy.array(c2l, dtype = "uint8")
    c2h = numpy.array(c2h, dtype = "uint8")
    c3l = numpy.array(c3l, dtype = "uint8")
    c3h = numpy.array(c3h, dtype = "uint8")
    c4l = numpy.array(c4l, dtype = "uint8")
    c4h = numpy.array(c4h, dtype = "uint8")
    
    mask1 = cv2.inRange(frame, c1l, c1h)
    mask2 = cv2.inRange(frame, c2l, c2h)
    mask3 = cv2.inRange(frame, c3l, c3h)
    mask4 = cv2.inRange(frame, c4l, c4h)
    
    f1 = cv2.bitwise_or(frame, frame, mask = mask1)
    f2 = cv2.bitwise_or(frame, frame, mask = mask2)
    f3 = cv2.bitwise_or(frame, frame, mask = mask3)
    f4 = cv2.bitwise_or(frame, frame, mask = mask4)
    
    final = cv2.bitwise_or(f1, f2)
    final = cv2.bitwise_or(final, f3)
    fimg = cv2.bitwise_or(final, f4)
    
    cv2.imshow("Orginal", frame)
    cv2.imshow("Mask", fimg)
    
    keypress = cv2.waitKey(30)
    
cap.release()
cv2.destroyAllWindows()