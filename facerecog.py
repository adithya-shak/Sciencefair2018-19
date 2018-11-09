import cv2
from video import create_capture
#from common import clock, draw_str

# You probably need to adjust some of these:
video_src = 0
cascade_fn = "haarcascade_frontalface_default.xml"
# Create a new CascadeClassifier from given cascade file:
cascade = cv2.CascadeClassifier(cascade_fn)
cam = create_capture(video_src)

while True:
  ret, img = cam.read()
  # Do a little preprocessing:
  img_copy = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
  gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
  gray = cv2.equalizeHist(gray)
  # Detect the faces (probably research for the options!):
  rects = cascade.detectMultiScale(gray)
  # Make a copy as we don't want to draw on the original image:
  for x, y, width, height in rects:
    cv2.rectangle(img_copy, (x, y), (x+width, y+height), (255,0,0), 2)
  cv2.imshow('facedetect', img_copy)
  if cv2.waitKey(20) == 27:
    break
