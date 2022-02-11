import cv2
import numpy
import os
import sys
import ctypes
import time
starttime = time.time()

ver = "0.1.3"
screen = ctypes.windll.user32

class eventcolors:
    WARNING = '\033[91mWarning: '
    DEBUG = '\033[90mDebug: '
    PASS = '\033[92mInfo: '
    CLB = '\033[95mCalibration: '
    CEN = '\033[95mCentroid: '
    TIMER = '\033[91mRun Time: '
    ENDC = '\033[0m'
    
print(f"{eventcolors.DEBUG}Starting CAPTv" + ver + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Current Dir: "+ os.getcwd() + f"{eventcolors.ENDC}")

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

cv2.moveWindow('Orginal',0,0)
cv2.moveWindow('Mask',640,0)
cv2.moveWindow('CTRL1',40,510)
cv2.moveWindow('CTRL2',340,510)
cv2.moveWindow('CTRL3',640,510)
cv2.moveWindow('CTRL4',940,510)

hhigh = 255
shigh = 255
vhigh = 255

cv2.createTrackbar("H Min", "CTRL1", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL1", 0, shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL1", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL1", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL1", shigh, shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL1", vhigh, vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL2", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL2", 0, shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL2", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL2", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL2", shigh, shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL2", vhigh, vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL3", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL3", 0, shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL3", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL3", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL3", shigh, shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL3", vhigh, vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL4", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL4", 0, shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL4", 0, vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL4", 0, hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL4", shigh, shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL4", vhigh, vhigh, lambda x:None)

cv2.createTrackbar("Mask", "CTRL1", 1, 1, lambda x:None)
cv2.createTrackbar("Mask", "CTRL2", 1, 1, lambda x:None)
cv2.createTrackbar("Mask", "CTRL3", 1, 1, lambda x:None)
cv2.createTrackbar("Mask", "CTRL4", 1, 1, lambda x:None)

keypress = 1

kernel = numpy.ones((5,5), numpy.uint8)

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
    
    mask1 = cv2.inRange(hsvframe, c1l, c1h)
    mask2 = cv2.inRange(hsvframe, c2l, c2h)
    mask3 = cv2.inRange(hsvframe, c3l, c3h)
    mask4 = cv2.inRange(hsvframe, c4l, c4h)
    
    f1 = cv2.bitwise_or(hsvframe, hsvframe, mask = mask1)
    f2 = cv2.bitwise_or(hsvframe, hsvframe, mask = mask2)
    f3 = cv2.bitwise_or(hsvframe, hsvframe, mask = mask3)
    f4 = cv2.bitwise_or(hsvframe, hsvframe, mask = mask4)
    
    gframe1 = cv2.cvtColor(f1,cv2.COLOR_BGR2GRAY)
    gframe2 = cv2.cvtColor(f2,cv2.COLOR_BGR2GRAY)
    gframe3 = cv2.cvtColor(f3,cv2.COLOR_BGR2GRAY)
    gframe4 = cv2.cvtColor(f4,cv2.COLOR_BGR2GRAY)
    
    gframe1 = cv2.erode(gframe1, kernel, iterations=1)
    gframe2 = cv2.erode(gframe2, kernel, iterations=1)
    gframe3 = cv2.erode(gframe3, kernel, iterations=1)
    gframe4 = cv2.erode(gframe4, kernel, iterations=1)
    
    mc1 = cv2.moments(gframe1)
    mc2 = cv2.moments(gframe2)
    mc3 = cv2.moments(gframe3)
    mc4 = cv2.moments(gframe4)
    
    if mc1["m00"] != 0:
        ctx1 = mc1["m10"]/mc1["m00"]
        cty1 = mc1["m01"]/mc1["m00"]
    else:
        ctx1 = 1
        cty1 = 1
    
    if mc2["m00"] != 0:
        ctx2 = mc2["m10"]/mc2["m00"]
        cty2 = mc2["m01"]/mc2["m00"]
    else:
        ctx2 = 1
        cty2 = 1
        
    if mc3["m00"] != 0:
        ctx3 = mc3["m10"]/mc3["m00"]
        cty3 = mc3["m01"]/mc3["m00"]
    else:
        ctx3 = 1
        cty3 = 1
        
    if mc4["m00"] != 0:
        ctx4 = mc4["m10"]/mc4["m00"]
        cty4 = mc4["m01"]/mc4["m00"]
    else:
        ctx4 = 1
        cty4 = 1
        
    print(f"{eventcolors.CEN}1: x:" + str(ctx1) + " y:" + str(cty1) + f"{eventcolors.ENDC}")
    print(f"{eventcolors.CEN}2: x:" + str(ctx2) + " y:" + str(cty2) + f"{eventcolors.ENDC}")
    print(f"{eventcolors.CEN}3: x:" + str(ctx3) + " y:" + str(cty3) + f"{eventcolors.ENDC}")
    print(f"{eventcolors.CEN}4: x:" + str(ctx4) + " y:" + str(cty4) + f"{eventcolors.ENDC}")
    
    cv2.circle(frame,(int(ctx1),int(cty1)),10,(255,0,0),-1)
    cv2.circle(frame,(int(ctx2),int(cty2)),10,(0,255,0),-1)
    cv2.circle(frame,(int(ctx3),int(cty3)),10,(0,0,255),-1)
    cv2.circle(frame,(int(ctx4),int(cty4)),10,(255,255,255),-1)
    
    #Selects the mask to be shown
    if cv2.getTrackbarPos("Mask", "CTRL1") == 1:
        final = f1
        if cv2.getTrackbarPos("Mask", "CTRL2") == 1:
            final = cv2.bitwise_or(final, f2)
        if cv2.getTrackbarPos("Mask", "CTRL3") == 1:
            final = cv2.bitwise_or(final, f3)
        if cv2.getTrackbarPos("Mask", "CTRL4") == 1:
            final = cv2.bitwise_or(final, f4)
    else:
        if cv2.getTrackbarPos("Mask", "CTRL2") == 1:
            final = f2
            if cv2.getTrackbarPos("Mask", "CTRL3") == 1:
                final = cv2.bitwise_or(final, f3)
            if cv2.getTrackbarPos("Mask", "CTRL4") == 1:
                final = cv2.bitwise_or(final, f4)
        else:
            if cv2.getTrackbarPos("Mask", "CTRL3") == 1:
                final = f3
                if cv2.getTrackbarPos("Mask", "CTRL4") == 1:
                    final = cv2.bitwise_or(final, f4)
            else:
                if cv2.getTrackbarPos("Mask", "CTRL4") == 1:
                    final = f4
                else:
                    final[:] = (0, 0, 0)
                    final = cv2.putText(final, "No Mask Is Enabled", (170,240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,95,155), 5, cv2.LINE_AA)
    fimg = final
    
    fimg = cv2.cvtColor(fimg,cv2.COLOR_HSV2BGR)
    
    print(f"{eventcolors.TIMER}", int((time.time() - starttime) / 60), ":", int((time.time() - starttime) - int((time.time() - starttime) / 60)) , f"{eventcolors.ENDC}")
    
    cv2.imshow("Orginal", frame)
    cv2.imshow("Mask", fimg)
    
    keypress = cv2.waitKey(30)
    
cap.release()
cv2.destroyAllWindows()
