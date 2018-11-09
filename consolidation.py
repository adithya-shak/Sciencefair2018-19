from __future__ import print_function
import os
import numpy as np
import cv2 as cv

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

cap = cv.VideoCapture(0)
cap2 = cv.VideoCapture(2)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
cap2.set(3,640) # set Width
cap2.set(4,480) # set Height

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret, frame2 = cap2.read()
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('right',gray)
    cv.imshow('left',gray2)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
