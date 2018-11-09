import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt
import time


cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
cap2.set(3,640) # set Width
cap2.set(4,480) # set Height
# Check if camera opened successfully
if (cap.isOpened()== False and cap2.isOpened()== False):
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened() and cap2.isOpened()):

    #if __name__ == '__main__':
        #imgL = cv2.imread('left.jpg')  # downscale images for faster processing
        #imgR = cv2.imread('actuallyleft.jpg')
  # Capture frame-by-frame
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    if ret == True and ret2 == True:

    # Display the resulting frame
        cv2.imshow('Frame',frame)
        cv2.imshow('Frame2',frame2)
        #framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame2gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('Gray1', framegray)
        #cv2.imshow('Gray2', frame2gray)
        #stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
        #disparity = stereo.compute(framegray, frame2gray)
        #minVal, maxVal, randval, dontcare = cv2.minMaxLoc(disparity)
        #disparity.convertTo(dispweird, CV_8UC1, 255.0/(maxVal - minVal), -minVal * 255.0/(maxVal - minVal));
        #disparitywithcolor = cv2.applyColorMap(dispweird, cv2.COLORMAP_JET)
        #plt.imshow(disparity,'disparity')
        #plt.show()
        #time.sleep(1)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
    else:
      break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
