import cv2

# Definitions
USE_WEBCAM = False
ASSET_LOC = "assets\\example_images\\"
IMAGE_LOC = ASSET_LOC + "BlueGoal-132in-Center.jpg"

# Filter Values
hue = [50.0, 96.0]
sat = [100.0, 255.0]
val = [78.0, 255.0]


def processImage(img):
    imgResize = cv2.resize(img, (640,480), 0, 0, cv2.INTER_CUBIC)
    imgBlur = cv2.GaussianBlur(imgResize, (7,7), 1)
    imgColorFilter = cv2.inRange(cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV), (hue[0], sat[0], val[0]),  (hue[1], sat[1], val[1]))
    cv2.imshow("blur", imgBlur)
    cv2.imshow("filter", imgColorFilter)
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
    main()