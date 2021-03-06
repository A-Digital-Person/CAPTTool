import cv2
import numpy
import os
import sys

ver = "0.1.1"

class eventcolors:
    WARNING = '\033[91mWarning: '
    DEBUG = '\033[90mDebug: '
    PASS = '\033[92mInfo: '
    CLB = '\033[95mCalibration: '
    ENDC = '\033[0m'

print(f"{eventcolors.DEBUG}Starting CAPTv" + ver + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Current Dir: "+ os.getcwd() + f"{eventcolors.ENDC}")

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

cv2.createTrackbar("Red Min", "CTRL1", 0, 255, lambda x:None)
cv2.createTrackbar("Green Min", "CTRL1", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Min", "CTRL1", 0, 255, lambda x:None)

cv2.createTrackbar("Red Max", "CTRL1", 0, 255, lambda x:None)
cv2.createTrackbar("Green Max", "CTRL1", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Max", "CTRL1", 0, 255, lambda x:None)

cv2.createTrackbar("Red Min", "CTRL2", 0, 255, lambda x:None)
cv2.createTrackbar("Green Min", "CTRL2", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Min", "CTRL2", 0, 255, lambda x:None)

cv2.createTrackbar("Red Max", "CTRL2", 0, 255, lambda x:None)
cv2.createTrackbar("Green Max", "CTRL2", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Max", "CTRL2", 0, 255, lambda x:None)

cv2.createTrackbar("Red Min", "CTRL3", 0, 255, lambda x:None)
cv2.createTrackbar("Green Min", "CTRL3", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Min", "CTRL3", 0, 255, lambda x:None)

cv2.createTrackbar("Red Max", "CTRL3", 0, 255, lambda x:None)
cv2.createTrackbar("Green Max", "CTRL3", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Max", "CTRL3", 0, 255, lambda x:None)

cv2.createTrackbar("Red Min", "CTRL4", 0, 255, lambda x:None)
cv2.createTrackbar("Green Min", "CTRL4", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Min", "CTRL4", 0, 255, lambda x:None)

cv2.createTrackbar("Red Max", "CTRL4", 0, 255, lambda x:None)
cv2.createTrackbar("Green Max", "CTRL4", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Max", "CTRL4", 0, 255, lambda x:None)

keypress = 1

while (keypress != 27):
    ret, frame = cap.read()
    c1rl = cv2.getTrackbarPos("Red Min", "CTRL1")
    c1gl = cv2.getTrackbarPos("Green Min", "CTRL1")
    c1bl = cv2.getTrackbarPos("Blue Min", "CTRL1")
    c1rh = cv2.getTrackbarPos("Red Max", "CTRL1")
    c1gh = cv2.getTrackbarPos("Green Max", "CTRL1")
    c1bh = cv2.getTrackbarPos("Blue Max", "CTRL1")
    
    c2rl = cv2.getTrackbarPos("Red Min", "CTRL2")
    c2gl = cv2.getTrackbarPos("Green Min", "CTRL2")
    c2bl = cv2.getTrackbarPos("Blue Min", "CTRL2")
    c2rh = cv2.getTrackbarPos("Red Max", "CTRL2")
    c2gh = cv2.getTrackbarPos("Green Max", "CTRL2")
    c2bh = cv2.getTrackbarPos("Blue Max", "CTRL2")
    
    c3rl = cv2.getTrackbarPos("Red Min", "CTRL3")
    c3gl = cv2.getTrackbarPos("Green Min", "CTRL3")
    c3bl = cv2.getTrackbarPos("Blue Min", "CTRL3")
    c3rh = cv2.getTrackbarPos("Red Max", "CTRL3")
    c3gh = cv2.getTrackbarPos("Green Max", "CTRL3")
    c3bh = cv2.getTrackbarPos("Blue Max", "CTRL3")
    
    c4rl = cv2.getTrackbarPos("Red Min", "CTRL4")
    c4gl = cv2.getTrackbarPos("Green Min", "CTRL4")
    c4bl = cv2.getTrackbarPos("Blue Min", "CTRL4")
    c4rh = cv2.getTrackbarPos("Red Max", "CTRL4")
    c4gh = cv2.getTrackbarPos("Green Max", "CTRL4")
    c4bh = cv2.getTrackbarPos("Blue Max", "CTRL4")
    
    c1l = [c1bl,c1gl,c1rl]
    c1h = [c1bh,c1gh,c1rh]
    
    c2l = [c2bl,c2gl,c2rl]
    c2h = [c2bh,c2gh,c2rh]

    c3l = [c3bl,c3gl,c3rl]
    c3h = [c3bh,c3gh,c3rh]
    
    c4l = [c4bl,c4gl,c4rl]
    c4h = [c4bh,c4gh,c4rh]
    
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
