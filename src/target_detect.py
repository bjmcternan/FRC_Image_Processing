import cv2

# Definitions
USE_WEBCAM = False
ASSET_LOC = "assets\\example_images\\"
IMAGE_LOC = ASSET_LOC + "BlueGoal-132in-Center.jpg"

# Filter Values
hue = [50.0, 96.0]
sat = [100.0, 255.0]
val = [78.0, 255.0]

def empty(a):
    pass

def createThresholdWindows():
    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 640,640)
    cv2.createTrackbar("hueMin", "Parameters", (int)(hue[0]),180,empty)
    cv2.createTrackbar("hueMax", "Parameters", (int)(hue[1]),180,empty)
    cv2.createTrackbar("satMin", "Parameters", (int)(sat[0]),255,empty)
    cv2.createTrackbar("satMax", "Parameters", (int)(sat[1]),255,empty)
    cv2.createTrackbar("valMin", "Parameters", (int)(val[0]),255,empty)
    cv2.createTrackbar("valMax", "Parameters", (int)(val[1]),255,empty)
    cv2.createTrackbar("ContourThreshold1", "Parameters", 150,255,empty)
    cv2.createTrackbar("ContourThreshold2", "Parameters", 255,255,empty)


def processImage(img):
    
    thresh1 = cv2.getTrackbarPos("ContourThreshold1", "Parameters")
    thresh2 = cv2.getTrackbarPos("ContourThreshold2", "Parameters")
    hueMin = cv2.getTrackbarPos("hueMin", "Parameters")
    hueMax = cv2.getTrackbarPos("hueMax", "Parameters")
    satMin = cv2.getTrackbarPos("satMin", "Parameters")
    satMax = cv2.getTrackbarPos("satMax", "Parameters")
    valMin = cv2.getTrackbarPos("valMin", "Parameters")
    valMax = cv2.getTrackbarPos("valMax", "Parameters")
    
    imgResize = cv2.resize(img, (640,480), 0, 0, cv2.INTER_CUBIC)
    imgBlur = cv2.GaussianBlur(imgResize, (7,7), 1)
    imgColorFilter = cv2.inRange(cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV), (hueMin, satMin, valMin),  (hueMax, satMax, valMax))
    imgCanny = cv2.Canny(imgColorFilter, thresh1, thresh2)
    cv2.imshow("blur", imgBlur)
    cv2.imshow("filter", imgColorFilter)
    cv2.imshow("Canny", imgCanny)
    output = imgColorFilter
    return output

def main():
    rval = False
    if USE_WEBCAM:
        cv2.namedWindow("preview")
        vc = cv2.VideoCapture(0)

        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False
    else:
        frame = cv2.imread(IMAGE_LOC)
        rval = True

    while rval:
        if USE_WEBCAM:
            rval, frame = vc.read()
            
        outImg = processImage(frame)

        key = cv2.waitKey(20)
        if key != -1: # exit on ESC
            break
    cv2.destroyWindow("preview")

if __name__=="__main__":
    createThresholdWindows()
    main()