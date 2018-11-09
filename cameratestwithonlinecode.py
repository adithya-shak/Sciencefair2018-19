import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt

min_disp = 16
if sys.argv[1] > 0:
    min_disp = int(sys.argv[1])
num_disp = 112 - min_disp
window_size = 17
cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)
# Check if camera opened successfully
if (cap.isOpened()== False and cap2.isOpened()== False):
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened() and cap2.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  ret2, frame2 = cap2.read()
  if ret == True and ret2 == True:

    # Display the resulting frame
    cv2.imshow('Frame',frame)
    cv2.imshow('Frame2',frame2)
    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame2gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Gray1', framegray)
    cv2.imshow('Gray2', frame2gray)
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(framegray, frame2gray)
    plt.imshow(disparity,'disparity')
    plt.show()
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
