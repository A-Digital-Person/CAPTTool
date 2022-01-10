import sys
cap = cv2.VideoCapture(0)
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(1)
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(2)
        if cap is None or not cap.isOpened():
            print("WARNING: Can't find a camera pluged in.")
            print("Check if your device is pluged into the device all the way")
            sys.exit()
        else:
            print("Cam found on port 2")
            camport = 2
    else:
        print("Cam found on port 1")
        camport = 1
else:
    print("Cam found on port 0")
    camport = 0
