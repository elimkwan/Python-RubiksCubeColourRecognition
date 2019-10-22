import cv2
import numpy as np

"""

Running this script will produced blackout images with tiles whiten out. 
The coordinate of the center of each tile will be labelled on the image as well.
The coordinate information will help calibrate the colourRegHSV.py script. 


DEMO: https://elimkwan.github.io/2019/08/05/cube/

"""

w_total = 1280
h_total = 960

Arr=[]

im = cv2.imread('down.jpg')
im = cv2.bilateralFilter(im,9,75,75)
im = cv2.fastNlMeansDenoisingColored(im,None,10,10,7,21)
hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)   # HSV image


#Calibarated range for the up Camera

COLOR_MIN = np.array([0, 80, 80],np.uint8)       # HSV color code lower and upper bounds
COLOR_MAX = np.array([180, 255, 255],np.uint8)   # filter all black and white

GREEN_COLOUR_MIN = np.array([90, 80, 80])
GREEN_COLOUR_MAX = np.array([105, 255, 255])    # filter all but green

YELLOW_COLOUR_MIN = np.array([30, 80, 80])
YELLOW_COLOUR_MAX = np.array([60, 255, 255])    # filter all but yellow

BLUE_COLOUR_MIN = np.array([105, 80, 80])
BLUE_COLOUR_MAX = np.array([180, 255, 255])    # filter all but blue

ORANGE_COLOUR_MIN = np.array([7, 80, 80])
ORANGE_COLOUR_MAX = np.array([30, 255, 255])    # filter all but orange

RED_COLOUR_MIN = np.array([0, 80, 80])
RED_COLOUR_MAX = np.array([20, 255, 255])    # filter all but red

WHITE_COLOUR_MIN = np.array([0, 0, 0])
WHITE_COLOUR_MAX = np.array([180, 80, 255])    # filter all but white

frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)     # Thresholding image
imgray = frame_threshed
ret,thresh = cv2.threshold(frame_threshed,127,255,0)
im,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# print type(contours)
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    if w > 10 and h > 10:
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)

        Cx = int(x + w/2)
        Cy = int(y + h/2)

        Cx_percentage = int(Cx/w_total*100)
        Cy_percentage = int(Cy/h_total*100)

        print(Cx, Cy, w, h)

        Arr.append([Cx , Cy])

        font = cv2.FONT_HERSHEY_SIMPLEX
        textposition = (Cx, Cy)
        textposition2 = (Cx, Cy+12)
        text = '{} {}'.format(Cx,Cy)
        fontColor = (0, 255, 255)

        cv2.putText(im, str(Cx_percentage), textposition,font,0.5,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(im, str(Cy_percentage), textposition2, font,0.5, (0, 0, 255), 1, cv2.LINE_AA)



print(*Arr, sep = ", ")

cv2.imshow("Show",im)
cv2.imwrite("down_extracted.jpg", im)
cv2.waitKey()
cv2.destroyAllWindows()