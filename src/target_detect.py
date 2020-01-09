import cv2
from grip import GripPipeline

# Using webcam
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

grip = GripPipeline()

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    # cv2.imshow("preview", frame)
    rval, frame = vc.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    cv2.inRange(frame, (0,0,128),  (180,255,255))
    cv2.imshow("RGB", frame)
    grip.process(frame)
    print(grip.find_blobs_output)
    # cv2.imshow("output", frame)

    key = cv2.waitKey(20)
    if key != -1: # exit on ESC
        break
cv2.destroyWindow("preview")