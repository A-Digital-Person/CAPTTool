import cv2
import numpy
import os
import sys
import ctypes
import time
import math
import tkinter as tk
from tkinter import *
from datetime import datetime
import re
import webbrowser
import shutil
import pysine
import yaml
base = """
  color1:
    hl: 0
    sl: 0
    vl: 0
    hh: 0
    sh: 255
    vh: 255
    mask: False
  color2:
    hl: 0
    sl: 0
    vl: 0
    hh: 0
    sh: 255
    vh: 255
    mask: False
  color3:
    hl: 0
    sl: 0
    vl: 0
    hh: 0
    sh: 255
    vh: 255
    mask: False
  color4:
    hl: 0
    sl: 0
    vl: 0
    hh: 0
    sh: 255
    vh: 255
    mask: False
  text:
    r: 255
    g: 255
    b: 255
  scale:
    dot: 10
    line: 5
  targets:
    min: 0
    max: 180
  blackout: False
"""
baseraw = {'color1': {'hl': 0, 'sl': 0, 'vl': 0, 'hh': 0, 'sh': 255, 'vh': 255, 'mask': 1}, 'color2': {'hl': 0, 'sl': 0, 'vl': 0, 'hh': 0, 'sh': 255, 'vh': 255, 'mask': 1}, 'color3': {'hl': 0, 'sl': 0, 'vl': 0, 'hh': 0, 'sh': 255, 'vh': 255, 'mask': 1}, 'color4': {'hl': 0, 'sl': 0, 'vl': 0, 'hh': 0, 'sh': 255, 'vh': 255, 'mask': 1}, 'text': {'r': 255, 'g': 255, 'b': 255}, 'scale': {'dot': 10, 'line': 5}, 'targets': {'min': 0, 'max': 180}, 'blackout': 0}
starttime = time.time()
astarttime = time.time()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists(os.getcwd() + '/logs'):
    os.makedirs(os.getcwd() + '/logs') 
loglocation = "logs/" + str(datetime.now()) + '.log'
loglocation = re.sub(':', '', loglocation)
sys.stdout = open(str(loglocation), 'x')

ver = "0.1.10"
screen = ctypes.windll.user32

class logtypes:
    WARNING = str(datetime.now()) + ' [Warning]: '
    ERROR = str(datetime.now()) + ' [ERROR]: '
    DEBUG = str(datetime.now()) + ' [Debug]: '
    INFO = str(datetime.now()) + ' [Info]: '
    CLB = str(datetime.now()) + ' [Calibration]: '
    CEN = str(datetime.now()) + ' [Centroid]: '
    TIMER = str(datetime.now()) + ' [Session Timer]: '
    
print(f"{logtypes.INFO}Starting CAPTv" + ver + f"")
print(f"{logtypes.INFO}Current Dir: "+ os.getcwd() + f"")

if os.path.exists(os.getcwd() + '/persistent.yml'):
    print(f"{logtypes.DEBUG}Using last session")
else:
    print(f"{logtypes.DEBUG}No session found. Creating new...")
    p = open('persistent.yml', 'w')
    yaml.dump(baseraw, p)
    #p.write("Color1HSV\n0\n0\n0\n0\n255\n255\nColor2\n0\n0\n0\n0\n255\n255\nColor3\n0\n0\n0\n0\n255\n255\nColor4\n0\n0\n0\n0\n255\n255\nOther\n255\n0\n255\n1\n1\n1\n1\n10\n5\n0\n0\n180\n")
    p.close()
    
def trycam():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
    
if True:
    cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(1)
        if cap is None or not cap.isOpened():
            cap = cv2.VideoCapture(2)
            if cap is None or not cap.isOpened():
                def nothing():
                    pass
                print(f"{logtypes.WARNING}Can't find a camera pluged in")
                print(f"{logtypes.DEBUG}Check if your device is pluged into the device all the way")
                master = Tk()
                master.lift()
                master.geometry("400x150")
                master.eval('tk::PlaceWindow . center')
                master.title('No Camera Error')
                l1 = Label(master, text = "Can't find a camera pluged in!",fg='#f00')
                l1.config(font =("Courier", 16))
                l2 = Label(master, text = "Check if your device is pluged ",fg='#f00')
                l2.config(font =("Courier", 14))
                l3 = Label(master, text = "into the device all the way.",fg='#f00')
                l3.config(font =("Courier", 14))
                b1 = Button(master, text = 'Try Again', width = 30, command=lambda: trycam())
                b2 = Button(master, text = 'Quit', width = 30, command=lambda: sys.exit())
                l1.pack()
                l2.pack()
                l3.pack()
                b1.pack()
                b2.pack()
                mainloop()
            else:
                print(f"{logtypes.INFO}Cam found on port 2")
                camport = 2
        else:
            print(f"{logtypes.INFO}Cam found on port 1")
            camport = 1
    else:
        print(f"{logtypes.INFO}Cam found on port 0")
        camport = 0
        
mintarget = 0
maxtarget = 180

allow = False
showerror = False
showerror2 = False
showerror3 = False
    
mintarget_var = 0
maxtarget_var = 0
while not allow:
    sys.stdout.close()
    sys.stdout = open(str(loglocation), 'a')
    master = Tk()
    master.lift()
    master.geometry("400x400")
    master.eval('tk::PlaceWindow . center')
    master.title('CAPT Start')
    mintarget_var = tk.StringVar()
    maxtarget_var = tk.StringVar()

    def usethis():
        global mintarget
        global maxtarget
        mintarget = mintarget_var.get()
        maxtarget = maxtarget_var.get()
        master.destroy()
    helpshown = False
    def openwiki():
        global helpshown
        url = 'https://example.com'
        webbrowser.open(url)
        if not helpshown:
            wiki = Label(master, text = "For help go to: " + str(url),fg='#ff4000')
            wiki.config(font =("Courier", 10))
            wiki.pack()
            helpshown = True
    l1 = Label(master, text = "CAPT Start!",fg='#0015ff')
    l1.config(font =("Courier", 16, 'bold', 'underline'))
    l2 = Label(master, text = "Enter the value of the dimentions",fg='#000')
    l2.config(font =("Courier", 12, 'bold'))
    l3 = Label(master, text = "you would like to use (0-180).",fg='#000')
    l3.config(font =("Courier", 12, 'bold'))
    l4 = Label(master, text = "This can be changed later.",fg='#000')
    l4.config(font =("Courier", 10))
    if showerror:
        error = Label(master, text = "Entry is not an integer!",fg='#ff0000')
        error.config(font =("Courier", 12, 'bold'))
        error2 = Label(master, text = "Please use a whole number 0-180.",fg='#ff0000')
        error2.config(font =("Courier", 12, 'bold'))
    if showerror2:
        error = Label(master, text = "Entry is the same!",fg='#ff0000')
        error.config(font =("Courier", 12, 'bold'))
        error2 = Label(master, text = "Please use a different values.",fg='#ff0000')
        error2.config(font =("Courier", 12, 'bold'))
    if showerror3:
        error = Label(master, text = "Entry is not in range!",fg='#ff0000')
        error.config(font =("Courier", 12, 'bold'))
        error2 = Label(master, text = "Please use a whole number 0-180.",fg='#ff0000')
        error2.config(font =("Courier", 12, 'bold'))
    mintar = tk.Label(master, text = 'Enter Your Min Target', font=('Courier',10, 'bold'))
    minentry = tk.Entry(master,textvariable = mintarget_var, font=('Courier',10,'normal'))
    maxtar = tk.Label(master, text = 'Enter Your Max Target', font=('Courier',10, 'bold'))
    maxentry = tk.Entry(master,textvariable = maxtarget_var, font=('Courier',10,'normal'))
    def uselast():
        p = open('persistent.yml', 'r')
        per = yaml.safe_load(p)
        minentry.delete(0,END)
        minentry.insert(0,str(per['targets']['min']))
        maxentry.delete(0,END)
        maxentry.insert(0,str(per['targets']['max']))
    def yeswipeeverything():
        sys.stdout.close()
        os.remove('persistent.yml')
        shutil.rmtree('logs')
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    def wipeeverything():
        master.destroy()
        reset = Tk()
        reset.lift()
        reset.geometry("400x400")
        reset.eval('tk::PlaceWindow . center')
        reset.title('RESET ALL DATA!')
        warn1 = Label(reset, text = "WARNING:",fg='#ff0000')
        warn1.config(font =("Courier", 12, 'bold'))
        warn2 = Label(reset, text = "Reseting will remove all log and",fg='#ff0000')
        warn2.config(font =("Courier", 12, 'bold'))
        warn3 = Label(reset, text = "data files from this computer!",fg='#ff0000')
        warn3.config(font =("Courier", 12, 'bold'))
        warn4 = Label(reset, text = "Do you want to do this!",fg='#ff0000')
        warn4.config(font =("Courier", 16, 'bold'))
        warn1.pack()
        warn2.pack()
        warn3.pack()
        warn4.pack()
        rb1 = Button(reset, text = 'Yes', width = 20, fg='#00731e', command=lambda: yeswipeeverything())
        rb2 = Button(reset, text = 'No', width = 20, fg='#ff0000', command=lambda: trycam())
        rb1.pack()
        rb2.pack()
    
    b1 = Button(master, text = 'Start Session', width = 20, fg='#00731e', command=lambda: usethis())
    b2 = Button(master, text = 'Use Last Session', width = 20, command=lambda: uselast())
    b3 = Button(master, text = 'Open Help Wiki', width = 20, fg='#1d00c2', command=lambda: openwiki())
    b4 = Button(master, text = 'Reset All Data', width = 20, fg='#ff0000', command=lambda: wipeeverything())
    b5 = Button(master, text = 'Quit', width = 20, command=lambda: sys.exit())
    l1.pack()
    l2.pack()
    l3.pack()
    l4.pack()
    if showerror:
        error.pack()
        error2.pack()
    if showerror2:
        error.pack()
        error2.pack()
    if showerror3:
        error.pack()
        error2.pack()
    mintar.pack()
    minentry.pack()
    maxtar.pack()
    maxentry.pack()
    b1.pack()
    b2.pack()
    b3.pack()
    b4.pack()
    b5.pack()
    mainloop()
    try:
         mintarget = int(mintarget)
         maxtarget = int(maxtarget)
    except:
        allow = False
        showerror = True
        showerror2 = False
        showerror3 = False
    else:
        if mintarget >= 0:
            if maxtarget <= 180:
                if mintarget != maxtarget:
                    allow = True
                else:
                    showerror = False
                    showerror2 = True
                    showerror3 = False
            else:
                showerror = False
                showerror2 = False
                showerror3 = True
        else:
            showerror = False
            showerror2 = False
            showerror3 = True
            
starttime = time.time()
bstarttime = time.time()

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

p = open('persistent.yml', 'r')
per = yaml.safe_load(p)

cv2.createTrackbar("H Min", "CTRL1", int(per['color1']['hl']), hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL1", int(per['color1']['sl']), shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL1", int(per['color1']['vl']), vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL1", int(per['color1']['hh']), hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL1", int(per['color1']['sh']), shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL1", int(per['color1']['vh']), vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL2", int(per['color2']['hl']), hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL2", int(per['color2']['sl']), shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL2", int(per['color2']['vl']), vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL2", int(per['color2']['hh']), hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL2", int(per['color2']['sh']), shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL2", int(per['color2']['vh']), vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL3", int(per['color3']['hl']), hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL3", int(per['color3']['sl']), shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL3", int(per['color3']['vl']), vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL3", int(per['color3']['hh']), hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL3", int(per['color3']['sh']), shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL3", int(per['color3']['vh']), vhigh, lambda x:None)

cv2.createTrackbar("H Min", "CTRL4", int(per['color4']['hl']), hhigh, lambda x:None)
cv2.createTrackbar("S Min", "CTRL4", int(per['color4']['sl']), shigh, lambda x:None)
cv2.createTrackbar("V Min", "CTRL4", int(per['color4']['vl']), vhigh, lambda x:None)

cv2.createTrackbar("H Max", "CTRL4", int(per['color4']['hh']), hhigh, lambda x:None)
cv2.createTrackbar("S Max", "CTRL4", int(per['color4']['sh']), shigh, lambda x:None)
cv2.createTrackbar("V Max", "CTRL4", int(per['color4']['vh']), vhigh, lambda x:None)

cv2.createTrackbar("Target Min", "OTHER", int(mintarget), 180, lambda x:None)
cv2.createTrackbar("Target Max", "OTHER", int(maxtarget), 180, lambda x:None)
cv2.createTrackbar("Blackout", "OTHER", int(per['blackout']), 1, lambda x:None)
cv2.createTrackbar("Text R", "OTHER", int(per['text']['r']), 255, lambda x:None)
cv2.createTrackbar("Text G", "OTHER", int(per['text']['g']), 255, lambda x:None)
cv2.createTrackbar("Text B", "OTHER", int(per['text']['b']), 255, lambda x:None)
cv2.createTrackbar("Dot Scale", "OTHER", int(per['scale']), 20, lambda x:None)
cv2.createTrackbar("Line Scale", "OTHER", int(per['scale']), 20, lambda x:None)

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
    return int(beta)
        

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
        
#     print(f"{logtypes.CEN}1: x:" + str(ctx1) + " y:" + str(cty1) + f"")
#     print(f"{logtypes.CEN}2: x:" + str(ctx2) + " y:" + str(cty2) + f"")
#     print(f"{logtypes.CEN}3: x:" + str(ctx3) + " y:" + str(cty3) + f"")
#     print(f"{logtypes.CEN}4: x:" + str(ctx4) + " y:" + str(cty4) + f"")

    cv2.circle(frame,(int(ctx1),int(cty1)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
    cv2.circle(frame,(int(ctx2),int(cty2)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
    cv2.circle(frame,(int(ctx3),int(cty3)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
    cv2.circle(frame,(int(ctx4),int(cty4)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
    
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
    showerror = False
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
                        showerror = True
    fimg = final
    
    fimg = cv2.cvtColor(fimg,cv2.COLOR_HSV2BGR)
    if showerror:
        fimg = cv2.putText(fimg, "No Mask Enabled", (190,240), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)

    
    if cv2.getTrackbarPos("Mask", "CTRL1") == 1:
        cv2.circle(fimg,(int(ctx1),int(cty1)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
        cv2.circle(fimg,(int(ctx1),int(cty1)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(255,0,0),-1)
    if cv2.getTrackbarPos("Mask", "CTRL2") == 1:
        cv2.circle(fimg,(int(ctx2),int(cty2)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
        cv2.circle(fimg,(int(ctx2),int(cty2)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(0,255,0),-1)
    if cv2.getTrackbarPos("Mask", "CTRL3") == 1:
        cv2.circle(fimg,(int(ctx3),int(cty3)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
        cv2.circle(fimg,(int(ctx3),int(cty3)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(0,0,255),-1)
    if cv2.getTrackbarPos("Mask", "CTRL4") == 1:
        cv2.circle(fimg,(int(ctx4),int(cty4)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
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
        print(f"{logtypes.ERROR}Can't calculate angle")
        
    
    mintarget = cv2.getTrackbarPos("Target Min", "OTHER")
    maxtarget = cv2.getTrackbarPos("Target Max", "OTHER")
    
    if int(angle) <= mintarget:
        frame = cv2.putText(frame, "WARN: UNDER", (3,117), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
        frame = cv2.putText(frame, "WARN: UNDER", (3,117), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
        pysine.sine(500, 0.1)
    elif int(angle) >= maxtarget:
        frame = cv2.putText(frame, "WARN: OVER", (3,117), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
        frame = cv2.putText(frame, "WARN: OVER", (3,117), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
        pysine.sine(700, 0.1)
        
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

fortimer = int( ((time.time() - astarttime)/60))*60
fortimer = str( int((time.time() - astarttime)/60) ) + ":" + str( int(time.time() - astarttime)-int(fortimer) ).zfill(2)

print(f"{logtypes.INFO}Program ended after running for " + str(fortimer))

fortimer = int( ((time.time() - bstarttime)/60))*60
fortimer = str( int((time.time() - bstarttime)/60) ) + ":" + str( int(time.time() - bstarttime)-int(fortimer) ).zfill(2)

print(f"{logtypes.INFO}The tracking timer run for " + str(fortimer))
sys.stdout.close()
cv2.destroyAllWindows()
sys.exit()