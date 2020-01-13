import cv2
import numpy as np

# Definitions
USE_WEBCAM = False
ASSET_LOC = "assets\\example_images\\"
IMAGE_LOC = ASSET_LOC + "BlueGoal-108in-Center.jpg"

# Initial Filter Values
hue = [50.0, 96.0]
sat = [100.0, 255.0]
val = [78.0, 255.0]

def empty(a):
    pass

def createThresholdWindows():
    # Setup window to hold paramteres sliders
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

def drawContours(img, contours):
    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        # draw a green rectangle to visualize the bounding rect
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.line(img, ((int)(w/2+x-10), (int)(h/2+y-10)), ((int)(w/2+x+10), (int)(h/2+y+10)), (255,0,255), 4)
        cv2.line(img, ((int)(w/2+x+10), (int)(h/2+y-10)), ((int)(w/2+x-10), (int)(h/2+y+10)), (255,0,255), 4)

def processImage(img):
    # Get parameters from slider window "Parameters"
    imgCopy = img.copy()
    thresh1 = cv2.getTrackbarPos("ContourThreshold1", "Parameters")
    thresh2 = cv2.getTrackbarPos("ContourThreshold2", "Parameters")
    hueMin = cv2.getTrackbarPos("hueMin", "Parameters")
    hueMax = cv2.getTrackbarPos("hueMax", "Parameters")
    satMin = cv2.getTrackbarPos("satMin", "Parameters")
    satMax = cv2.getTrackbarPos("satMax", "Parameters")
    valMin = cv2.getTrackbarPos("valMin", "Parameters")
    valMax = cv2.getTrackbarPos("valMax", "Parameters")
    
    # Resize image to make workspace smaller 
    imgResize = cv2.resize(img, (640,480), 0, 0, cv2.INTER_CUBIC)
    # Slightly blur imaage to get rid of some noise 
    imgBlur = cv2.GaussianBlur(imgResize, (7,7), 1)
    # Convert image to HSV and filter based off of hue, sat, and val
    imgColorFilter = cv2.inRange(cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV), (hueMin, satMin, valMin),  (hueMax, satMax, valMax))
    # Run Canny contour detector to find contours in image
    #imgCanny = cv2.Canny(imgColorFilter, thresh1, thresh2)
    contours, hierarchy = cv2.findContours(imgColorFilter, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    drawContours(imgCopy, contours)
    # Show output
    previewImg = np.concatenate((imgColorFilter, imgCopy), axis=1)
    cv2.imshow("Contours", previewImg)
    output = imgColorFilter
    return output

def main():
    rval = False
    if USE_WEBCAM:
        cv2.namedWindow("preview")
        vc = cv2.VideoCapture(0)

        if vc.isOpened(): 
            # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False
    else:
        # read image from disk
        frame = cv2.imread(IMAGE_LOC)
        rval = True

    while rval:
        if USE_WEBCAM:
            rval, frame = vc.read()
        
        # Process image
        outImg = processImage(frame)

        key = cv2.waitKey(20)
        if key != -1: # exit on any key press
            break
    cv2.destroyWindow("preview")

if __name__=="__main__":
    createThresholdWindows()
    main()
