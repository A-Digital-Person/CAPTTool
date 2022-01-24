import cv2
import numpy
import os
import sys
import ctypes
import time
import math
from datetime import datetime
import re
starttime = time.time()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists(os.getcwd() + '/logs'):
    os.makedirs(os.getcwd() + '/logs') 
loglocation = "logs/" + str(datetime.now()) + '.log'
loglocation = re.sub(':', '', loglocation)
sys.stdout = open(str(loglocation), 'x')

ver = "0.1.10"
screen = ctypes.windll.user32

class eventcolors:
    WARNING = str(datetime.now()) + ' [Warning]: '
    ERROR = str(datetime.now()) + ' [ERROR]: '
    DEBUG = str(datetime.now()) + ' [Debug]: '
    PASS = str(datetime.now()) + ' [Info]: '
    CLB = str(datetime.now()) + ' [Calibration]: '
    CEN = str(datetime.now()) + ' [Centroid]: '
    TIMER = str(datetime.now()) + ' [Session Timer]: '
    ENDC = ''
    

    
print(f"{eventcolors.DEBUG}Starting CAPTv" + ver + f"{eventcolors.ENDC}")
print(f"{eventcolors.DEBUG}Current Dir: "+ os.getcwd() + f"{eventcolors.ENDC}")

if os.path.exists(os.getcwd() + '/persistent.capt'):
    print(f"{eventcolors.DEBUG}Using last session{eventcolors.ENDC}")
else:
    print(f"{eventcolors.DEBUG}No session found. Creating new...{eventcolors.ENDC}")
    p = open('persistent.capt', 'w')
    p.write("Color1HSV\n0\n0\n0\n0\n255\n255\nColor2\n0\n0\n0\n0\n255\n255\nColor3\n0\n0\n0\n0\n255\n255\nColor4\n0\n0\n0\n0\n255\n255\nOther\n255\n0\n255\n1\n1\n1\n1\n10\n5\n0\n0\n120\n")
    p.close()

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
cv2.namedWindow("OTHER")

cv2.resizeWindow("CTRL1", 285, 320)
cv2.resizeWindow("CTRL2", 285, 320)
cv2.resizeWindow("CTRL3", 285, 320)
cv2.resizeWindow("CTRL4", 285, 320)
cv2.resizeWindow("OTHER", 285, 320)

cv2.moveWindow('Orginal',0,0)
cv2.moveWindow('Mask',640,0)
cv2.moveWindow('CTRL1',0,510)
cv2.moveWindow('CTRL2',285,510)
cv2.moveWindow('CTRL3',570,510)
cv2.moveWindow('CTRL4',855,510)
cv2.moveWindow('OTHER',1140,510)

hhigh = 180
shigh = 255
vhigh = 255

p = open('persistent.capt', 'r')
per = p.readlines()

cv2.createTrackbar("H Min", "CTRL1", int(per[1]), hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL1", int(per[2]), shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL1", int(per[3]), vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL1", int(per[4]), hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL1", int(per[5]), shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL1", int(per[6]), vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL2", int(per[8]), hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL2", int(per[9]), shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL2", int(per[10]), vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL2", int(per[11]), hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL2", int(per[12]), shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL2", int(per[13]), vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL3", int(per[15]), hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL3", int(per[16]), shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL3", int(per[17]), vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL3", int(per[18]), hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL3", int(per[19]), shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL3", int(per[20]), vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL4", int(per[22]), hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL4", int(per[23]), shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL4", int(per[24]), vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL4", int(per[25]), hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL4", int(per[26]), shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL4", int(per[27]), vhigh, lambda x:None)

cv2.createTrackbar("Target Min", "OTHER", int(per[39]), 1, lambda x:None)
cv2.createTrackbar("Target Max", "OTHER", int(per[40]), 1, lambda x:None)
cv2.createTrackbar("Blackout", "OTHER", int(per[38]), 1, lambda x:None)
cv2.createTrackbar("Text R", "OTHER", int(per[29]), 255, lambda x:None)
cv2.createTrackbar("Text G", "OTHER", int(per[30]), 255, lambda x:None)
cv2.createTrackbar("Text B", "OTHER", int(per[31]), 255, lambda x:None)
cv2.createTrackbar("Dot Scale", "OTHER", int(per[36]), 20, lambda x:None)
cv2.createTrackbar("Line Scale", "OTHER", int(per[37]), 20, lambda x:None)

def close(x):
    cv2.setTrackbarPos("Blackout", "OTHER", 0)

cv2.createTrackbar("Mask", "CTRL1", int(per[32]), 1, close)
cv2.createTrackbar("Mask", "CTRL2", int(per[33]), 1, close)
cv2.createTrackbar("Mask", "CTRL3", int(per[34]), 1, close)
cv2.createTrackbar("Mask", "CTRL4", int(per[35]), 1, close)

keypress = 1

kernel = numpy.ones((10,10), numpy.uint8)

frame = 0

def getang(c1x,c1y,c2x,c2y,c3x,c3y,c4x,c4y):
    global frame
    c1x = float(c1x)
    c1y = float(c1y)
    c2x = float(c2x)
    c2y = float(c2y)
    c3x = float(c3x)
    c3y = float(c3y)
    c4x = float(c4x)
    c4y = float(c4y)
    
    if (c4x <= c3x) or (c4y >= c3y):
        beta = 0
        frame = cv2.putText(frame, "ERROR: Wrong Quadrant", (3,87), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
        frame = cv2.putText(frame, "ERROR: Wrong Quadrant", (3,87), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
    else:
        if (c1x == c2x) and (c1y < c2y):
            angleFA = 0
        elif (c1x == c2x) and (c1y > c2y):
            angleFA = math.pi
        elif c1y == c2y:
            angleFA = math.pi/2
        else:
            angleFA = math.atan((abs(c1x-c2x))/(abs(c1y-c2y)))
        
        if (c4x == c3x) and (c4y < c3y):
            angleUA = 0
        elif (c4x == c3x) and (c4y > c3y):
            angleUA = 90
        else:
            angleUA = math.atan((abs(c3x-c4x))/(abs(c3y-c4y)))
            
        if (c1x>=c2x) and (c1y<c2y) and (c4x>=c3x) and (c4y<c3y):
            beta = angleUA - angleFA
        elif (c1x<c2x) and (c1y<=c2y) and (c4x>=c3x) and (c4y<c3y):
            beta = angleUA + angleFA
        elif (c1x<=c2x) and (c1y>c2y) and (c4x>=c3x) and (c4y<c3y):
            beta = math.pi - angleFA + angleUA
        else:
            frame = cv2.putText(frame, "ERROR: Wrong Pos", (3,87), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
            frame = cv2.putText(frame, "ERROR: Wrong Pos", (3,87), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
    beta = beta * (180/math.pi)
    alpha = 180 - beta
    alpha = '%.0f'%(alpha)
    return alpha
        

while (keypress != 27):
    ret, frame = cap.read()
    
    if keypress == ord('r'):
        starttime = time.time()
    
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
    
    gframe1 = cv2.dilate(gframe1,kernel,iterations = 1)
    gframe2 = cv2.dilate(gframe2,kernel,iterations = 1)
    gframe3 = cv2.dilate(gframe3,kernel,iterations = 1)
    gframe4 = cv2.dilate(gframe4,kernel,iterations = 1)
    
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
        
#     print(f"{eventcolors.CEN}1: x:" + str(ctx1) + " y:" + str(cty1) + f"{eventcolors.ENDC}")
#     print(f"{eventcolors.CEN}2: x:" + str(ctx2) + " y:" + str(cty2) + f"{eventcolors.ENDC}")
#     print(f"{eventcolors.CEN}3: x:" + str(ctx3) + " y:" + str(cty3) + f"{eventcolors.ENDC}")
#     print(f"{eventcolors.CEN}4: x:" + str(ctx4) + " y:" + str(cty4) + f"{eventcolors.ENDC}")
    
    cv2.circle(frame,(int(ctx1),int(cty1)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(255,0,0),-1)
    cv2.circle(frame,(int(ctx2),int(cty2)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(0,255,0),-1)
    cv2.circle(frame,(int(ctx3),int(cty3)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(0,0,255),-1)
    cv2.circle(frame,(int(ctx4),int(cty4)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(255,255,255),-1)
    
    if cv2.getTrackbarPos("Line Scale", "OTHER") == 0:
        cv2.setTrackbarPos("Line Scale", "OTHER", 1)
    
    frame = cv2.line(frame, (int(ctx1),int(cty1)), (int(ctx2),int(cty2)), (0,0,0), cv2.getTrackbarPos("Line Scale", "OTHER")+5)
    frame = cv2.line(frame, (int(ctx3),int(cty3)), (int(ctx4),int(cty4)), (0,0,0), cv2.getTrackbarPos("Line Scale", "OTHER")+5)
    frame = cv2.line(frame, (int(ctx1),int(cty1)), (int(ctx2),int(cty2)), (255,255,255), cv2.getTrackbarPos("Line Scale", "OTHER"))
    frame = cv2.line(frame, (int(ctx3),int(cty3)), (int(ctx4),int(cty4)), (255,255,255), cv2.getTrackbarPos("Line Scale", "OTHER"))

    #Selects the mask to be shown
    final = f1
    if cv2.getTrackbarPos("Blackout", "OTHER") == 1:
        final[:] = (0, 0, 0)
    if cv2.getTrackbarPos("Blackout", "OTHER") == 0:
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
    
    if cv2.getTrackbarPos("Mask", "CTRL1") == 1:
        cv2.circle(fimg,(int(ctx1),int(cty1)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(255,0,0),-1)
    if cv2.getTrackbarPos("Mask", "CTRL2") == 1:
        cv2.circle(fimg,(int(ctx2),int(cty2)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(0,255,0),-1)
    if cv2.getTrackbarPos("Mask", "CTRL3") == 1:
        cv2.circle(fimg,(int(ctx3),int(cty3)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(0,0,255),-1)
    if cv2.getTrackbarPos("Mask", "CTRL4") == 1:
        cv2.circle(fimg,(int(ctx4),int(cty4)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(255,255,255),-1)
        
    if (cv2.getTrackbarPos("Mask", "CTRL1") == 1) and (cv2.getTrackbarPos("Mask", "CTRL2") == 1):
        fimg = cv2.line(fimg, (int(ctx1),int(cty1)), (int(ctx2),int(cty2)), (0,0,0), cv2.getTrackbarPos("Line Scale", "OTHER")+5)
        fimg = cv2.line(fimg, (int(ctx1),int(cty1)), (int(ctx2),int(cty2)), (255,255,255), cv2.getTrackbarPos("Line Scale", "OTHER"))
    if cv2.getTrackbarPos("Mask", "CTRL3") == 1 and cv2.getTrackbarPos("Mask", "CTRL4") == 1:
        fimg = cv2.line(fimg, (int(ctx3),int(cty3)), (int(ctx4),int(cty4)), (0,0,0), cv2.getTrackbarPos("Line Scale", "OTHER")+5)
        fimg = cv2.line(fimg, (int(ctx3),int(cty3)), (int(ctx4),int(cty4)), (255,255,255), cv2.getTrackbarPos("Line Scale", "OTHER"))
    
    fortimer = int( ((time.time() - starttime)/60))*60
    
    fortimer = str( int((time.time() - starttime)/60) ) + ":" + str( int(time.time() - starttime)-int(fortimer) ).zfill(2)

    frame = cv2.putText(frame, "Session Time: " + fortimer, (3,27), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
    frame = cv2.putText(frame, "Session Time: " + fortimer, (3,27), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
    
    try:
        angle = getang(ctx1,cty1,ctx2,cty2,ctx3,cty3,ctx4,cty4)
        frame = cv2.putText(frame, "Angle: " + str(angle), (3,57), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
        frame = cv2.putText(frame, "Angle: " + str(angle), (3,57), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)

    except:
        frame = cv2.putText(frame, "ERROR: Calculating error", (3,57), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
        frame = cv2.putText(frame, "ERROR: Calculating error", (3,57), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
        print(f"{eventcolors.ERROR}Can't calculate angle{eventcolors.ENDC}")

    
    cv2.imshow("Orginal", frame)
    cv2.imshow("Mask", fimg)
    
    sys.stdout.close()
    sys.stdout = open(str(loglocation), 'a')
    
    keypress = cv2.waitKey(30)
    
cap.release()
p = open('persistent.capt', 'w')
#Color1HSV\n0\n0\n0\n0\n0\n0\nColor2\n0\n0\n0\n0\n0\n0\nColor3\n0\n0\n0\n0\n0\n0\nColor4\n0\n0\n0\n0\n0\n0\n
p.write("Color1HSV\n")
p.close()
p = open('persistent.capt', 'a')
p.write(str(cv2.getTrackbarPos("H Min", "CTRL1")) + "\n")
p.write(str(cv2.getTrackbarPos("S Min", "CTRL1")) + "\n")
p.write(str(cv2.getTrackbarPos("V Min", "CTRL1")) + "\n")
p.write(str(cv2.getTrackbarPos("H Max", "CTRL1")) + "\n")
p.write(str(cv2.getTrackbarPos("S Max", "CTRL1")) + "\n")
p.write(str(cv2.getTrackbarPos("V Max", "CTRL1")) + "\n")
p.write("Color2\n")
p.write(str(cv2.getTrackbarPos("H Min", "CTRL2")) + "\n")
p.write(str(cv2.getTrackbarPos("S Min", "CTRL2")) + "\n")
p.write(str(cv2.getTrackbarPos("V Min", "CTRL2")) + "\n")
p.write(str(cv2.getTrackbarPos("H Max", "CTRL2")) + "\n")
p.write(str(cv2.getTrackbarPos("S Max", "CTRL2")) + "\n")
p.write(str(cv2.getTrackbarPos("V Max", "CTRL2")) + "\n")
p.write("Color3\n")
p.write(str(cv2.getTrackbarPos("H Min", "CTRL3")) + "\n")
p.write(str(cv2.getTrackbarPos("S Min", "CTRL3")) + "\n")
p.write(str(cv2.getTrackbarPos("V Min", "CTRL3")) + "\n")
p.write(str(cv2.getTrackbarPos("H Max", "CTRL3")) + "\n")
p.write(str(cv2.getTrackbarPos("S Max", "CTRL3")) + "\n")
p.write(str(cv2.getTrackbarPos("V Max", "CTRL3")) + "\n")
p.write("Color4\n")
p.write(str(cv2.getTrackbarPos("H Min", "CTRL4")) + "\n")
p.write(str(cv2.getTrackbarPos("S Min", "CTRL4")) + "\n")
p.write(str(cv2.getTrackbarPos("V Min", "CTRL4")) + "\n")
p.write(str(cv2.getTrackbarPos("H Max", "CTRL4")) + "\n")
p.write(str(cv2.getTrackbarPos("S Max", "CTRL4")) + "\n")
p.write(str(cv2.getTrackbarPos("V Max", "CTRL4")) + "\n")
p.write("Other\n")
p.write(str(cv2.getTrackbarPos("Text R", "OTHER")) + "\n")
p.write(str(cv2.getTrackbarPos("Text G", "OTHER")) + "\n")
p.write(str(cv2.getTrackbarPos("Text B", "OTHER")) + "\n")
p.write(str(cv2.getTrackbarPos("Mask", "CTRL1")) + "\n")
p.write(str(cv2.getTrackbarPos("Mask", "CTRL2")) + "\n")
p.write(str(cv2.getTrackbarPos("Mask", "CTRL3")) + "\n")
p.write(str(cv2.getTrackbarPos("Mask", "CTRL4")) + "\n")
p.write(str(cv2.getTrackbarPos("Dot Scale", "OTHER")) + "\n")
p.write(str(cv2.getTrackbarPos("Line Scale", "OTHER")) + "\n")
p.write(str(cv2.getTrackbarPos("Blackout", "OTHER")) + "\n")
p.write(str(cv2.getTrackbarPos("Target Min", "OTHER")) + "\n")
p.write(str(cv2.getTrackbarPos("Target Max", "OTHER")) + "\n")
p.close()
sys.stdout.close()
cv2.destroyAllWindows()