import cv2
import numpy

cap = cv2.VideoCapture(0)

cv2.namedWindow("Orginal")
cv2.namedWindow("Mask")
cv2.namedWindow("CTRL")

cv2.resizeWindow("CTRL")

cv2.createTrackbar("Red Min", "CTRL", 0, 255, lambda x:None)
cv2.createTrackbar("Green Min", "CTRL", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Min", "CTRL", 0, 255, lambda x:None)

cv2.createTrackbar("Red Max", "CTRL", 0, 255, lambda x:None)
cv2.createTrackbar("Green Max", "CTRL", 0, 255, lambda x:None)
cv2.createTrackbar("Blue Max", "CTRL", 0, 255, lambda x:None)

keypress = 1

while (keypress != 27):
    ret, frame = cap.read()
    c1rl = cv2.getTrackbarPos("Red Min", "CTRL")
    c1gl = cv2.getTrackbarPos("Green Min", "CTRL")
    c1bl = cv2.getTrackbarPos("Blue Min", "CTRL")
    c1rh = cv2.getTrackbarPos("Red Max", "CTRL")
    c1gh = cv2.getTrackbarPos("Green Max", "CTRL")
    c1bh = cv2.getTrackbarPos("Blue Max", "CTRL")
    
    c1l = [c1bl,c1gl,c1rl]
    c1h = [c1bh,c1gh,c1br]
    
    c1l = numpy.array(c1l, dtype = "uint8")
    c1h = numpy.array(c1h, dtype = "uint8")
    
    mask1 = cv2.inRange(frame, c1l, c1h)
    
    fimg = cv2.bitwise_or(frame, frame, mask = mask1)
    
    cv2.imshow("Original", frame)
    cv2.imshow("Mask", fimg)
    
    keypress = cv2.waitKey(30)
    
cap.release()
cv2.destroyAllWindows()
