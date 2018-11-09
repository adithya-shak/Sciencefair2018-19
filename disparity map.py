import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.VideoCapture(2)
imgR = cv2.VideoCapture(3)


if (imgL.isOpened()== False or imgR.isOpened()== False):
  print("Error opening video stream or file")

# Read until video is completed
while(imgL.isOpened() and imgR.isOpened()):
  # Capture frame-by-frame

  ret, frame = imgL.read()
  ret2, frame2 = imgL.read()
  if ret & ret2 == True:


    cv2.imshow('img1', frame)
    cv2.imshow('img2', frame2)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    #cv2.imshow(frame,'gray1')
    #cv2.show()
    #cv2.imshow(frame2,'gray2')
    #cv2.show()
    #stereo = cv2.createStereoBM(numDisparities=16, blockSize=15)
    #disparity = stereo.compute(frame,frame2)
    #plt.imshow(disparity,'disparity')
    #plt.show()

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break

# When everything done, release the video capture object
#cap.release()

# Closes all the frames
cv2.destroyAllWindows()
