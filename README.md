# Rubiks Cube Colour Recognition Code written in Python

This code takes the input from 3 web cams and scans a Rubik's Cube. colourRegHSV.py will scan the sube, recognise the colour on each tile, and return a list that indicate the current state of the cube to Combined-Control.py. Combined-Control.py will run the logic that generate the moves to solve the Rubik's Cube and output corresponding analogue waveform(in the audio file) to the Embedded Circuit. Sound wave of different frequencies will then pass through an embedded circuit which then turn one of the 6 motors in clockwise/anticlockwise direction.  

For better result, can also calibrate the position of the cube with the script in calibration folder. The images in the folder shows the past calibration results. 

How to run the programme:
Run Combined-Control.py with the environment set up

Main features:
a) Utilise two colour spaces (RGB and HSV) instead of RGB only;
b) Use of random seed averaging approach, such that colour analysis would be carried out on random pixels within the tiles instead of fixed ones;
c) Calibrate targets’ locations with OpenCV edge detection and colour threshold functions.

DEMO: https://elimkwan.github.io/2019/08/05/cube/
