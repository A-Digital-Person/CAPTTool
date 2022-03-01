# Libs use:
# cv2 - Image manulipion lib
# numpy - Array creator
# os - File mangement
# sys - Stops program
# ctypes - Screen size
# time - Timer
# math - Angle caluclation
# tkinter - Opening menus
# datetime - Gets the current data and time
# re - Cleans the datetime for file names
# webbrowser - Opens the help page
# pysine - Plays the output tone
# ymal - Remembering session data mangement

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
import pysine
import yaml

#Opening message
os.system('color a')
print('CAPT Tool is starting!')
print('Please wait...')

# Sets data and time vars
baseraw = {'color1': {'hl': 76, 'sl': 74, 'vl': 120, 'hh': 110, 'sh': 255, 'vh': 255, 'mask': 1}, 'color2': {'hl': 32, 'sl': 86, 'vl': 78, 'hh': 76, 'sh': 195, 'vh': 176, 'mask': 1}, 'color3': {'hl': 6, 'sl': 128, 'vl': 0, 'hh': 30, 'sh': 255, 'vh': 255, 'mask': 1}, 'color4': {'hl': 117, 'sl': 104, 'vl': 0, 'hh': 141, 'sh': 255, 'vh': 255, 'mask': 1}, 'text': {'r': 255, 'g': 255, 'b': 255}, 'scale': {'dot': 10, 'line': 5}, 'targets': {'min': 0, 'max': 90}, 'blackout': 0}
starttime = time.time()
astarttime = time.time()

#Sets the data file for output
datafile = 'data/' + str(datetime.now()) + '.CAPTResults.csv'

#Fix derectory if running in python.
#Breaks if using exe.
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(os.getcwd())

#Create log and data dir and files if missing
if not os.path.exists(os.getcwd() + '/logs'):
    os.makedirs(os.getcwd() + '/logs')
loglocation = "logs/" + str(datetime.now()) + '.log'
loglocation = re.sub(':', '', loglocation)
sys.stdout = open(str(loglocation), 'x')

if not os.path.exists(os.getcwd() + '/data'):
    os.makedirs(os.getcwd() + '/data')
datafile = re.sub(':', '', datafile)

#Build and screen dimentions
ver = "1.0.3"
screen = ctypes.windll.user32

#Log file prefixes
class logtypes:
    WARNING = str(datetime.now()) + ' [Warning]: '
    ERROR = str(datetime.now()) + ' [ERROR]: '
    DEBUG = str(datetime.now()) + ' [Debug]: '
    INFO = str(datetime.now()) + ' [Info]: '
    CLB = str(datetime.now()) + ' [Calibration]: '
    CEN = str(datetime.now()) + ' [Centroid]: '
    TIMER = str(datetime.now()) + ' [Session Timer]: '

#Logfile starting
print(f"{logtypes.INFO}Starting CAPTv" + ver + f"")
print(f"{logtypes.INFO}Current Dir: "+ os.getcwd() + f"")

#Use old data if found
if os.path.exists(os.getcwd() + '/persistent.yml'):
    print(f"{logtypes.DEBUG}Using last session")
else:
    print(f"{logtypes.DEBUG}No session found. Creating new...")
    p = open('persistent.yml', 'w')
    yaml.dump(baseraw, p)
    #p.write("Color1HSV\n0\n0\n0\n0\n255\n255\nColor2\n0\n0\n0\n0\n255\n255\nColor3\n0\n0\n0\n0\n255\n255\nColor4\n0\n0\n0\n0\n255\n255\nOther\n255\n0\n255\n1\n1\n1\n1\n10\n5\n0\n0\n180\n")
    p.close()

#Restart program
def trycam():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

aviablecams = []
#Find the cam port
if True:
    cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        pass
    else:
        aviablecams.append("Port 0")
    cap = cv2.VideoCapture(1)
    if cap is None or not cap.isOpened():
        pass
    else:
        aviablecams.append("Port 1")
    cap = cv2.VideoCapture(2)
    if cap is None or not cap.isOpened():
        pass
    else:
        aviablecams.append("Port 2")
    
                
    cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(1)
        if cap is None or not cap.isOpened():
            cap = cv2.VideoCapture(2)
            if cap is None or not cap.isOpened():
                def nothing():
                    pass
                #Error screen
                print(f"{logtypes.WARNING}Can't find a camera plugged in")
                print(f"{logtypes.DEBUG}Check if your device is plugged into the device all the way")
                master = Tk()
                master.lift()
                master.geometry("400x150")
                master.eval('tk::PlaceWindow . center')
                master.title('No Camera Error')
                l1 = Label(master, text = "Can't find a camera plugged in!",fg='#f00')
                l1.config(font =("Courier", 16))
                l2 = Label(master, text = "Check if your device is plugged ",fg='#f00')
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
        else:
            print(f"{logtypes.INFO}Cam found on port 1")
    else:
        print(f"{logtypes.INFO}Cam found on port 0")

#Sets vars for later
mintarget = 0
maxtarget = 180

allow = False
showerror = False
showerror2 = False
showerror3 = False
    
mintarget_var = 0
maxtarget_var = 0
camport = 0

#Start window
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
        global camport
        mintarget = mintarget_var.get()
        maxtarget = maxtarget_var.get()
        if variable.get() == "Port 0":
            camport = 0
            print(f"{logtypes.DEBUG}Set camport to 0")
        elif variable.get() == "Port 1":
            camport = 1
            print(f"{logtypes.DEBUG}Set camport to 1")
        elif variable.get() == "Port 2":
            camport = 2
            print(f"{logtypes.DEBUG}Set camport to 2")
        master.destroy()
    helpshown = False
    def openwiki():
        global helpshown
        url = 'https://github.com/A-Digital-Person/CAPTTool/wiki'
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
    l3 = Label(master, text = "you would like to use (0-90).",fg='#000')
    l3.config(font =("Courier", 12, 'bold'))
    l4 = Label(master, text = "This can be changed later.",fg='#000')
    l4.config(font =("Courier", 10))
    if showerror:
        error = Label(master, text = "Entry is not an integer!",fg='#ff0000')
        error.config(font =("Courier", 12, 'bold'))
        error2 = Label(master, text = "Please use a whole number 0-90.",fg='#ff0000')
        error2.config(font =("Courier", 12, 'bold'))
    if showerror2:
        error = Label(master, text = "Entry is the same!",fg='#ff0000')
        error.config(font =("Courier", 12, 'bold'))
        error2 = Label(master, text = "Please use a different values.",fg='#ff0000')
        error2.config(font =("Courier", 12, 'bold'))
    if showerror3:
        error = Label(master, text = "Entry is not in range!",fg='#ff0000')
        error.config(font =("Courier", 12, 'bold'))
        error2 = Label(master, text = "Please use a whole number 0-90.",fg='#ff0000')
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
    variable = StringVar(master)
    variable.set(aviablecams[0])
    port = OptionMenu(master, variable, *aviablecams)
    port.pack()
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
            if maxtarget <= 90:
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

#Session timers
starttime = time.time()
bstarttime = time.time()

#Windoes creations
cv2.namedWindow("Orginal")
cv2.namedWindow("Mask")
cv2.namedWindow("CTRL1")
cv2.namedWindow("CTRL2")
cv2.namedWindow("CTRL3")
cv2.namedWindow("CTRL4")
cv2.namedWindow("OTHER")

#Resize windoes
cv2.resizeWindow("CTRL1", 285, 320)
cv2.resizeWindow("CTRL2", 285, 320)
cv2.resizeWindow("CTRL3", 285, 320)
cv2.resizeWindow("CTRL4", 285, 320)
cv2.resizeWindow("OTHER", 285, 320)

#Pos windoes
cv2.moveWindow('Orginal',0,0)
cv2.moveWindow('Mask',640,0)
cv2.moveWindow('CTRL1',0,510)
cv2.moveWindow('CTRL2',285,510)
cv2.moveWindow('CTRL3',570,510)
cv2.moveWindow('CTRL4',855,510)
cv2.moveWindow('OTHER',1140,510)

#Max values
hhigh = 180
shigh = 255
vhigh = 255

#Read session file and set old data to trackbars
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

cv2.createTrackbar("Target Min", "OTHER", int(mintarget), 90, lambda x:None)
cv2.createTrackbar("Target Max", "OTHER", int(maxtarget), 90, lambda x:None)
cv2.createTrackbar("Blackout", "OTHER", int(per['blackout']), 1, lambda x:None)
cv2.createTrackbar("Text R", "OTHER", int(per['text']['r']), 255, lambda x:None)
cv2.createTrackbar("Text G", "OTHER", int(per['text']['g']), 255, lambda x:None)
cv2.createTrackbar("Text B", "OTHER", int(per['text']['b']), 255, lambda x:None)
cv2.createTrackbar("Dot Scale", "OTHER", int(per['scale']['dot']), 20, lambda x:None)
cv2.createTrackbar("Line Scale", "OTHER", int(per['scale']['line']), 20, lambda x:None)

def close(x):
    cv2.setTrackbarPos("Blackout", "OTHER", 0)

cv2.createTrackbar("Mask", "CTRL1", int(per['color1']['mask']), 1, close)
cv2.createTrackbar("Mask", "CTRL2", int(per['color1']['mask']), 1, close)
cv2.createTrackbar("Mask", "CTRL3", int(per['color3']['mask']), 1, close)
cv2.createTrackbar("Mask", "CTRL4", int(per['color4']['mask']), 1, close)

#Base vars
keypress = 1
kernel = numpy.ones((10,10), numpy.uint8)
frame = 0

#Calc angle
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
            angleHA = 0
        elif (c1x == c2x) and (c1y > c2y):
            angleHA = math.pi/2
        elif c1y == c2y:
            angleHA = math.pi/2
        elif (c1x <= c2x) and (c1y <= c2y):
            angleHA = math.atan((abs(c1x-c2x))/(abs(c1y-c2y)))
        else:
            angleHA = math.atan((abs(c1y-c2y))/(abs(c1x-c2x)))
        if (c4x == c3x) and (c4y < c3y):
            angleFA = 0
        elif (c4y == c3y) and (c4x > c3x):
            angleFA = math.pi/2
        else:
            angleFA = math.atan((abs(c3x-c4x))/(abs(c3y-c4y)))
        if (c1x>=c2x) and (c1y<c2y) and (c4x>=c3x) and (c4y<c3y):
            beta = angleFA - angleHA
        elif (c1x<c2x) and (c1y<=c2y) and (c4x>=c3x) and (c4y<C3y):
            beta = angleHA + angleFA
        elif (c1x<=c2x) and (c1y>c2y) and (c4x>=c3x) and (c4y<c3y):
            beta = (math.pi - angleFA) + (math.pi/2 - angleHA)
        elif (c1x>c2x) and (c1y>=c2y) and (c4x>=c3x) and (c4y<c3y):
            beta = (math.pi/2 + angleHA) - angleFA
        else:
            beta = 0
            frame = cv2.putText(frame, "ERROR: Wrong Pos", (3,87), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
            frame = cv2.putText(frame, "ERROR: Wrong Pos", (3,87), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
            
    beta = beta * (180/math.pi)
    alpha = 180 - beta
    alpha = '%.0f'%(alpha)
    return int(alpha)

#Data every second
lastprint = 0

#Main loop
cap = cv2.VideoCapture(camport)
print(f"{logtypes.INFO}Using Camera on port: "+ str(camport))
while (keypress != 27):
    #Get cam data
    ret, frame = cap.read()
    
    #Reset session timer
    if keypress == ord('r'):
        starttime = time.time()
    
    #Set frame to hsv
    hsvframe = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    #Read trackbars
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
    
    #Set colors
    c1l = [c1hl,c1sl,c1vl]
    c1h = [c1hh,c1sh,c1vh]
    
    c2l = [c2hl,c2sl,c2vl]
    c2h = [c2hh,c2sh,c2vh]

    c3l = [c3hl,c3sl,c3vl]
    c3h = [c3hh,c3sh,c3vh]
    
    c4l = [c4hl,c4sl,c4vl]
    c4h = [c4hh,c4sh,c4vh]
    
    #Set arrays
    c1l = numpy.array(c1l, dtype = "uint8")
    c1h = numpy.array(c1h, dtype = "uint8")
    c2l = numpy.array(c2l, dtype = "uint8")
    c2h = numpy.array(c2h, dtype = "uint8")
    c3l = numpy.array(c3l, dtype = "uint8")
    c3h = numpy.array(c3h, dtype = "uint8")
    c4l = numpy.array(c4l, dtype = "uint8")
    c4h = numpy.array(c4h, dtype = "uint8")
    
    #Set mask
    mask1 = cv2.inRange(hsvframe, c1l, c1h)
    mask2 = cv2.inRange(hsvframe, c2l, c2h)
    mask3 = cv2.inRange(hsvframe, c3l, c3h)
    mask4 = cv2.inRange(hsvframe, c4l, c4h)
    
    #Clean pixels
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

    #Draw dots
    cv2.circle(frame,(int(ctx1),int(cty1)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
    cv2.circle(frame,(int(ctx2),int(cty2)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
    cv2.circle(frame,(int(ctx3),int(cty3)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
    cv2.circle(frame,(int(ctx4),int(cty4)),cv2.getTrackbarPos("Dot Scale", "OTHER") + 2,(0,0,0),-1)
    
    cv2.circle(frame,(int(ctx1),int(cty1)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(255,0,0),-1)
    cv2.circle(frame,(int(ctx2),int(cty2)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(0,255,0),-1)
    cv2.circle(frame,(int(ctx3),int(cty3)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(0,0,255),-1)
    cv2.circle(frame,(int(ctx4),int(cty4)),cv2.getTrackbarPos("Dot Scale", "OTHER"),(255,255,255),-1)
    
    #Fix line scale
    if cv2.getTrackbarPos("Line Scale", "OTHER") == 0:
        cv2.setTrackbarPos("Line Scale", "OTHER", 1)
    
    #Draw lines
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
    
    #Show text
    fimg = cv2.cvtColor(fimg,cv2.COLOR_HSV2BGR)
    if showerror:
        fimg = cv2.putText(fimg, "No Mask Enabled", (190,240), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)

    #Draw the dots
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
    
    #Draw the lines
    if (cv2.getTrackbarPos("Mask", "CTRL1") == 1) and (cv2.getTrackbarPos("Mask", "CTRL2") == 1):
        fimg = cv2.line(fimg, (int(ctx1),int(cty1)), (int(ctx2),int(cty2)), (0,0,0), cv2.getTrackbarPos("Line Scale", "OTHER")+5)
        fimg = cv2.line(fimg, (int(ctx1),int(cty1)), (int(ctx2),int(cty2)), (255,255,255), cv2.getTrackbarPos("Line Scale", "OTHER"))
    if cv2.getTrackbarPos("Mask", "CTRL3") == 1 and cv2.getTrackbarPos("Mask", "CTRL4") == 1:
        fimg = cv2.line(fimg, (int(ctx3),int(cty3)), (int(ctx4),int(cty4)), (0,0,0), cv2.getTrackbarPos("Line Scale", "OTHER")+5)
        fimg = cv2.line(fimg, (int(ctx3),int(cty3)), (int(ctx4),int(cty4)), (255,255,255), cv2.getTrackbarPos("Line Scale", "OTHER"))
    
    #Timer calc
    fortimer = int( ((time.time() - starttime)/60))*60
    
    fortimer = str( int((time.time() - starttime)/60) ) + ":" + str( int(time.time() - starttime)-int(fortimer) ).zfill(2)

    frame = cv2.putText(frame, "Session Time: " + fortimer, (3,27), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
    frame = cv2.putText(frame, "Session Time: " + fortimer, (3,27), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
    
    #Try calc angle
    try:
        angle = getang(ctx1,cty1,ctx2,cty2,ctx3,cty3,ctx4,cty4)
        frame = cv2.putText(frame, "Angle: " + str(angle), (3,57), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
        frame = cv2.putText(frame, "Angle: " + str(angle), (3,57), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)

    except:
        angle = 0
        frame = cv2.putText(frame, "ERROR: Calculating error", (3,57), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
        frame = cv2.putText(frame, "ERROR: Calculating error", (3,57), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
        print(f"{logtypes.ERROR}Can't calculate angle")
        
    #Target values
    mintarget = cv2.getTrackbarPos("Target Min", "OTHER") + 90
    maxtarget = cv2.getTrackbarPos("Target Max", "OTHER") + 90
    
    #Warnings for min and max
    if int(angle) <= mintarget:
        frame = cv2.putText(frame, "WARN: UNDER", (3,117), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
        frame = cv2.putText(frame, "WARN: UNDER", (3,117), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
        pysine.sine(500, 0.1)
    elif int(angle) >= maxtarget:
        frame = cv2.putText(frame, "WARN: OVER", (3,117), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5, cv2.LINE_AA)
        frame = cv2.putText(frame, "WARN: OVER", (3,117), cv2.FONT_HERSHEY_SIMPLEX, 1, (cv2.getTrackbarPos("Text B", "OTHER"),cv2.getTrackbarPos("Text G", "OTHER"),cv2.getTrackbarPos("Text R", "OTHER")), 2, cv2.LINE_AA)
        pysine.sine(700, 0.1)
    
    #Show frames
    cv2.imshow("Orginal", frame)
    cv2.imshow("Mask", fimg)
    
    #Slowdown data printing to file
    if lastprint != fortimer:
        p = open(datafile, 'a')
        p.write(str(datetime.now()) + ', ' + str(int(angle)) + '\n')
        p.close()
    lastprint = fortimer
    
    #Save all prints to log file
    sys.stdout.close()
    sys.stdout = open(str(loglocation), 'a')
    
    #Delay
    keypress = cv2.waitKey(30)

#Close program
cap.release()

#Save all trackbar data
p = open(r'persistent.yml', 'w')
saveraw = {'color1': {'hl': int(cv2.getTrackbarPos("H Min", "CTRL1")),
                      'sl': int(cv2.getTrackbarPos("S Min", "CTRL1")),
                      'vl': int(cv2.getTrackbarPos("V Min", "CTRL1")),
                      'hh': int(cv2.getTrackbarPos("H Max", "CTRL1")),
                      'sh': int(cv2.getTrackbarPos("S Max", "CTRL1")),
                      'vh': int(cv2.getTrackbarPos("V Max", "CTRL1")),
                      'mask': int(cv2.getTrackbarPos("Mask", "CTRL1"))},
           'color2': {'hl': int(cv2.getTrackbarPos("H Min", "CTRL2")),
                      'sl': int(cv2.getTrackbarPos("S Min", "CTRL2")),
                      'vl': int(cv2.getTrackbarPos("V Min", "CTRL2")),
                      'hh': int(cv2.getTrackbarPos("H Max", "CTRL2")),
                      'sh': int(cv2.getTrackbarPos("S Max", "CTRL2")),
                      'vh': int(cv2.getTrackbarPos("V Max", "CTRL2")),
                      'mask': int(cv2.getTrackbarPos("Mask", "CTRL2"))},
           'color3': {'hl': int(cv2.getTrackbarPos("H Min", "CTRL3")),
                      'sl': int(cv2.getTrackbarPos("S Min", "CTRL3")),
                      'vl': int(cv2.getTrackbarPos("V Min", "CTRL3")),
                      'hh': int(cv2.getTrackbarPos("H Max", "CTRL3")),
                      'sh': int(cv2.getTrackbarPos("S Max", "CTRL3")),
                      'vh': int(cv2.getTrackbarPos("V Max", "CTRL3")),
                      'mask': int(cv2.getTrackbarPos("Mask", "CTRL3"))},
           'color4': {'hl': int(cv2.getTrackbarPos("H Min", "CTRL4")),
                      'sl': int(cv2.getTrackbarPos("S Min", "CTRL4")),
                      'vl': int(cv2.getTrackbarPos("V Min", "CTRL4")),
                      'hh': int(cv2.getTrackbarPos("H Max", "CTRL4")),
                      'sh': int(cv2.getTrackbarPos("S Max", "CTRL4")),
                      'vh': int(cv2.getTrackbarPos("V Max", "CTRL4")),
                      'mask': int(cv2.getTrackbarPos("Mask", "CTRL4"))},
           'text': {'r': int(cv2.getTrackbarPos("Text R", "OTHER")),
                    'g': int(cv2.getTrackbarPos("Text G", "OTHER")),
                    'b': int(cv2.getTrackbarPos("Text B", "OTHER"))},
           'scale': {'dot': int(cv2.getTrackbarPos("Dot Scale", "OTHER")),
                     'line': int(cv2.getTrackbarPos("Line Scale", "OTHER"))},
           'targets': {'min':int(cv2.getTrackbarPos("Target Min", "OTHER")),
                       'max': int(cv2.getTrackbarPos("Target Max", "OTHER"))},
           'blackout': int(cv2.getTrackbarPos("Blackout", "OTHER"))}
yaml.dump(saveraw, p)
# p.write(saveme)
p.close()

#Timer calc to log
fortimer = int( ((time.time() - astarttime)/60))*60
fortimer = str( int((time.time() - astarttime)/60) ) + ":" + str( int(time.time() - astarttime)-int(fortimer) ).zfill(2)

print(f"{logtypes.INFO}Program ended after running for " + str(fortimer))

fortimer = int( ((time.time() - bstarttime)/60))*60
fortimer = str( int((time.time() - bstarttime)/60) ) + ":" + str( int(time.time() - bstarttime)-int(fortimer) ).zfill(2)

print(f"{logtypes.INFO}The tracking timer run for " + str(fortimer))

#Close everything and exit program
sys.stdout.close()
cv2.destroyAllWindows()
sys.exit()