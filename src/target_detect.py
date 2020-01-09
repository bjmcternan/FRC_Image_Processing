import cv2
import numpy as np
from grip import GripPipeline

# Using webcam
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

grip = GripPipeline()

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

curSatValDelta = 1
curSatVal = 0.0
while rval:
    # curSatVal = curSatVal + curSatValDelta;
    # if(curSatVal >= 255):
    #     curSatVal = 255
    #     curSatValDelta = curSatValDelta * -1
    # elif(curSatVal <= 0):
    #     curSatVal = 0
    #     curSatValDelta = curSatValDelta * -1

    grip.setThreshold([0.0,150])
    print(curSatVal)
    # cv2.imshow("preview", frame)
    rval, frame = vc.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # cv2.inRange(frame, (0,0,0),  (180,255,100))
    # cv2.imshow("RGB", cv2.cvtColor(frame, cv2.COLOR_HSV2BGR))
    grip.process(frame)
    hsvThresh = grip.hsv_threshold_output;
    # cv2.imshow("RGB", hsvThresh) #cv2.cvtColor(hsvThresh, cv2.COLOR_HSV2BGR))
    if(grip.find_blobs_output):
        frame = cv2.drawKeypoints(frame, grip.find_blobs_output, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # Show keypoints
    cv2.imshow("Keypoints", cv2.cvtColor(frame, cv2.COLOR_HSV2BGR))

    key = cv2.waitKey(20)
    if key != -1: # exit on ESC
        break
cv2.destroyWindow("preview")