# Rubiks Cube Colour Recognition Code written in Python

A group porject with Chris, Adam, Beth and AJ. My main contribution is with the colourRegHSV.py code and the hardware part. This code takes the input from 3 web cams and scans a Rubik's Cube. colourRegHSV.py will scan the sube, recognise the colour on each tile, and return a list that indicate the current state of the cube to Combined-Control.py. Combined-Control.py will run the logic that generate the moves to solve the Rubik's Cube and output corresponding analogue waveform(in the audio file) to the Embedded Circuit. Sound wave of different frequencies will then pass through an embedded circuit which then turn one of the 6 motors in clockwise/anticlockwise direction.  

For better result, can also calibrate the position of the cube with the script in calibration folder. The images in the folder shows the past calibration results. 

## Running the programme (without Webcam):
Comment out the following code in colourRegHSV.py
```
#when connected to camera
cap0 = cv2.VideoCapture(0)#up
cap1 = cv2.VideoCapture(1)#side
cap2 = cv2.VideoCapture(3)#down

ret, frame = cap0.read()
rgb_up = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
cv2.imshow('frame', rgb_up)
out = cv2.imwrite('up.jpg', frame)
cap0.release()
cv2.destroyAllWindows()
im = Image.open('up.jpg')  # 658x693

ret, frame = cap1.read()
rgb_side = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
cv2.imshow('frame', rgb_side)
out = cv2.imwrite('side.jpg', frame)
cap1.release()
cv2.destroyAllWindows()
im = Image.open('side.jpg')  # 658x693

ret, frame = cap2.read()
rgb_down = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
cv2.imshow('frame', rgb_down)
out = cv2.imwrite('down.jpg', frame)
cap2.release()
cv2.destroyAllWindows()
im = Image.open('down.jpg')  # 658x693
```
And uncomment the following code in colourRegHSV.py
```
#temp: when not connected to camera, use old images
#using opencv to load image x and y interchange!
rgb_down = cv2.imread("down.jpg")
rgb_side = cv2.imread("side.jpg")
rgb_up = cv2.imread("up.jpg")
```
Then, run Combined-Control.py with the environment set up
```
python Combined-Control.py
```


## Main features:
a) Utilise two colour spaces (RGB and HSV) instead of RGB only;
b) Use of random seed averaging approach, such that colour analysis would be carried out on random pixels within the tiles instead of fixed ones;
c) Calibrate targets’ locations with OpenCV edge detection and colour threshold functions.

DEMO: https://elimkwan.github.io/2019/08/05/cube/
