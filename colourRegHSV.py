import pprint
import cv2
import numpy as np
from PIL import Image
import math
from random import randint



"""

Running this script will provoke the 3 webcams connected to take pictures for analysis of the current state of the cube.
The script will conduct colour recognition and identify the colour of each tile of the Rubik's Cube.
The script will output an array that that is in the format e.g.""UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"" for Combined-Control.py


DEMO: https://elimkwan.github.io/2019/08/05/cube/

"""



def select_pix_array(local_camera_select):

    """

    A function that select 5 pixels samples from random positions on each tiles

    :param local_camera_select: the camera image
    :return: local_pix which is a 16 * 6 * 2 matrix that contained the x,y locations of the selected pixels from each tiles
    """

    d = 15
    h = 960 # 480
    w = 1280 # 640
    # from pix[0][0]
    # pix to [79][1] i.e. 80 sets of 2
    # THESE ARE TUPLES AS  "rgb_0 = (imL[local_pix[n]])" ONLY ACCEPTS TUPLES SO THEY CANNOT BE EDITED
    if local_camera_select == 'up':
        #center point of rectangle
        x = [38, 48, 58, 38, 58, 37, 48, 59, 37, 48, 59, 38, 58, 38, 48, 57]#percentage
        x = [int(w * i / 100) for i in x]
        y = [33, 35, 35, 41, 43, 50, 52, 53, 61, 62, 63, 70, 72, 78, 78, 80]#percentage
        y = [int(h * i / 100) for i in y]
    if local_camera_select == 'down':
        x = [41, 51, 60, 42, 61, 41, 51, 62, 41, 51, 62, 42, 62, 42, 52, 62]  # percentage
        x = [int(w * i / 100) for i in x]
        y = [25, 26, 25, 32, 33, 41, 42, 42, 51, 52, 52, 61, 61, 70, 70, 70]  # percentage
        y = [int(h * i / 100) for i in y]

    if local_camera_select == 'side':
        x = [40, 50, 59, 40, 60, 39, 50, 61, 39, 50, 61, 40, 60, 41, 51, 60]  # percentage
        x = [int(w * i / 100) for i in x]
        y = [26, 25, 25, 34, 33, 43, 43, 43, 53, 53, 53, 62, 62, 70, 70, 70]  # percentage
        y = [int(h * i / 100) for i in y]

    # e.g. 5 pixels sample collected for square zero
    #(x[0], y[0]), (x[0] + d, y[0] + d), (x[0] + d, y[0] - d), (x[0] - d, y[0] - d), (x[0] - d, y[0] + d),

    #j, w, h = 2, 5, 15
    #local_pix = [[0 for z in range (j) for x in range(w)] for y in range(h)]
    #print(*local_pix, sep = ",")

    a,b,c =2, 9, 16
    local_pix = [[[0 for col in range(a)] for col in range(b)] for row in range(c)]

    for i in range (0, 16):

        local_pix[i][0][0] = x[i]
        local_pix[i][0][1] = y[i]

        local_pix[i][1][0] = x[i] + randint(1, d)
        local_pix[i][1][1] = y[i] + randint(1, d)

        local_pix[i][2][0] = x[i] + randint(1, d)
        local_pix[i][2][1] = y[i] - randint(1, d)

        local_pix[i][3][0] = x[i] - randint(1, d)
        local_pix[i][3][1] = y[i] - randint(1, d)

        local_pix[i][4][0] = x[i] - randint(1, d)
        local_pix[i][4][1] = y[i] + randint(1, d)

        local_pix[i][5][0] = x[i] + randint(1, d)
        local_pix[i][5][1] = y[i]

        local_pix[i][6][0] = x[i]
        local_pix[i][6][1] = y[i] + randint(1, d)

        local_pix[i][3][0] = x[i] - randint(1, d)
        local_pix[i][3][1] = y[i]

        local_pix[i][4][0] = x[i]
        local_pix[i][4][1] = y[i] - randint(1, d)

        #pprint.pprint(local_pix)

    return local_pix

def average_hsv_of_each_tile(local_pix, rgb):

    """

    A function

    :param local_pix: the coordinates of the 5 selected samples from each tiles
    :param rgb: the raw image
    :return: hsv_array_per_camera which is an array that contains the averaged hsv value for each tiles
    """

    w, h = 3, 16
    hsv_array_per_camera = [[0 for x in range(w)] for y in range(h)]

    #loop from 16 square of the picture
    for n in range(0, 16):
        #each square have 5 samples (in RGB)
        Sample0 = rgb[local_pix[n][0][1],local_pix[n][0][0]]
        Sample1 = rgb[local_pix[n][1][1], local_pix[n][1][0]]
        Sample2 = rgb[local_pix[n][2][1], local_pix[n][2][0]]
        Sample3 = rgb[local_pix[n][3][1], local_pix[n][3][0]]
        Sample4 = rgb[local_pix[n][4][1], local_pix[n][4][0]]
        Sample5 = rgb[local_pix[n][5][1], local_pix[n][0][0]]
        Sample6 = rgb[local_pix[n][6][1], local_pix[n][1][0]]
        Sample7 = rgb[local_pix[n][7][1], local_pix[n][2][0]]
        Sample8 = rgb[local_pix[n][8][1], local_pix[n][3][0]]

        for j in range(0, 3):
            #when j = 0, average the B value of all 5 samples
            hsv_array_per_camera[n][j] = (int(Sample0[j]) + int(Sample1[j]) + int(Sample2[j]) + int(Sample3[j]) + int(Sample4[j]) + int(Sample5[j]) + int(Sample6[j])+ int(Sample7[j])+ int(Sample8[j])) / 9

        temp = cv2.cvtColor(np.uint8([[hsv_array_per_camera[n]]]), cv2.COLOR_BGR2HSV)
        hsv_array_per_camera[n] = temp[0][0]

    return hsv_array_per_camera

def colour_rec(faces, hsv_values):
    colour = str()

    #setting color range for all th faces
    #-------------------|-------U---------|---------R---------|---------F---------|--------D--------|--------L--------|---------B---------|
    V_threshold_all = [ 135,               150,               138,               140,               140,               130]
    cold_H_range_all = [[35, 95, 145] ,    [35, 95, 145] ,    [35, 95, 145] ,    [35, 95, 145] ,    [35, 95, 145],     [35, 95, 145] ]#red, green, blue
    warm_H_range_all = [[25, 52, 95, 145], [25, 52, 95, 145], [25, 52, 95, 145], [25, 52, 95, 145], [25, 52, 95, 145], [25, 52, 95, 145]] #orange, yellow, green(lower priority), blue(lower priority)
    S_min_all = [        40,                40,                40,                20,                15,                40]

    cold_H_range = []
    warm_H_range = []

    #S_min = 40  # all colours s should be bigger than 45 except white tiles
    if faces == "U":
        cold_H_range = cold_H_range_all[0]
        warm_H_range = warm_H_range_all[0]
        S_min = S_min_all[0]
        V_threshold = V_threshold_all[0]
    elif faces == "R":
        cold_H_range = cold_H_range_all[1]
        warm_H_range = warm_H_range_all[1]
        S_min = S_min_all[1]
        V_threshold = V_threshold_all[1]
    elif faces == "F":
        cold_H_range = cold_H_range_all[2]
        warm_H_range = warm_H_range_all[2]
        S_min = S_min_all[2]
        V_threshold = V_threshold_all[2]
    elif faces == "D":
        cold_H_range = cold_H_range_all[3]
        warm_H_range = warm_H_range_all[3]
        S_min = S_min_all[3]
        V_threshold = V_threshold_all[3]
    elif faces == "L":
        cold_H_range = cold_H_range_all[4]
        warm_H_range = warm_H_range_all[4]
        S_min = S_min_all[4]
        V_threshold = V_threshold_all[4]
    else: #B
        cold_H_range = cold_H_range_all[5]
        warm_H_range = warm_H_range_all[5]
        S_min = S_min_all[5]
        V_threshold = V_threshold_all[5]



    #cold_H_range = [15, 45, 95, 145] #red, yellow, green, blue
    #cold_H_range = [35, 95, 145] #yellow, green, blue
    #warm_H_range = [25, 52, 95, 145] #orange, yellow, green(lower priority), blue(lower priority), red(lower priority)
    S_orange = 185
    H_orange = 110

    for n in range(0, 9):
        #hsv_values[n][0]#H
        #hsv_values[n][1]#S
        #hsv_values[n][2]#V

        if hsv_values[n][1] >= S_min:
            if hsv_values[n][2] >= V_threshold:
                #warm
                # ORANGE
                if  hsv_values[n][0] <= warm_H_range[0]:
                    value = "O"
                # YELLOW
                elif hsv_values[n][0] <= warm_H_range[1]:
                    value = "Y"
                # GREEN lower priority )
                elif hsv_values[n][0] <= warm_H_range[2]:
                    value = "G"
                # BLUE(lower priority )
                elif hsv_values[n][0] <= warm_H_range[3]:
                    value = "B"
                # RED(lower priority )
                else:
                    value = "R"

            else:
                #cold
                # RED
                if (hsv_values[n][0] <= cold_H_range[0] or hsv_values[n][0] >= cold_H_range[2]):
                    value = "R"
                    if (hsv_values[n][1]>= S_orange) and (hsv_values[n][2]>= H_orange):
                        value = "O"
                #GREEN
                elif (hsv_values[n][0] <= cold_H_range[1]):
                    value = "G"
                # BLUE
                else:
                    value = "B"
        else:
            #WHITE
            value = "W"
    

        print('{} {} {} {}'.format(value, str(hsv_values[n][0]), str(hsv_values[n][1]), str(hsv_values[n][2])), end="   ")
        colour = colour + value

    print("\n")
    return colour

def formatstr(in_string):
    """

    A function to change the string from using colour as face representation to using the standard format "U","R","F","D","L","B"

    :param in_string: an array with "Y","O","G","W","R","B" to indicate different face on the cube
    :return: an array with "U","R","F","D","L","B" to indicate different face on the cube
    """

    output = ""
    seq_pos = ["U","R","F","D","L","B"] #position
    seq_col = ["Y","O","G","W","R","B"] #colour
    for item in in_string:
        for i in range(0, len(seq_pos)):
            if item == seq_col[i]:
                output = output + str(seq_pos[i])
    #print(output)
    return (output)

def reorder_string(in_string):
    """

    A function to reorder the string into the format that Combined-Control.py required

    :param in_string: a list of "Y","O","G","W","R","B"
    :return: a list of "Y","O","G","W","R","B"
    """

    #U
    out_string = in_string[2]
    out_string = out_string + in_string[5]
    out_string = out_string + in_string[8]
    out_string = out_string + in_string[1]
    out_string = out_string + in_string[4]
    out_string = out_string + in_string[7]
    out_string = out_string + in_string[0]
    out_string = out_string + in_string[3]
    out_string = out_string + in_string[6]

    #R
    out_string = out_string + in_string[9]
    out_string = out_string + in_string[10]
    out_string = out_string + in_string[11]
    out_string = out_string + in_string[12]
    out_string = out_string + in_string[13]
    out_string = out_string + in_string[14]
    out_string = out_string + in_string[15]
    out_string = out_string + in_string[16]
    out_string = out_string + in_string[17]

    #F
    out_string = out_string + in_string[20]
    out_string = out_string + in_string[23]
    out_string = out_string + in_string[26]
    out_string = out_string + in_string[19]
    out_string = out_string + in_string[22]
    out_string = out_string + in_string[25]
    out_string = out_string + in_string[18]
    out_string = out_string + in_string[21]
    out_string = out_string + in_string[24]

    #D
    out_string = out_string + in_string[35]
    out_string = out_string + in_string[34]
    out_string = out_string + in_string[33]
    out_string = out_string + in_string[32]
    out_string = out_string + in_string[31]
    out_string = out_string + in_string[30]
    out_string = out_string + in_string[29]
    out_string = out_string + in_string[28]
    out_string = out_string + in_string[27]

    #L starting 36
    out_string = out_string + in_string[38]
    out_string = out_string + in_string[41]
    out_string = out_string + in_string[44]
    out_string = out_string + in_string[37]
    out_string = out_string + in_string[40]
    out_string = out_string + in_string[43]
    out_string = out_string + in_string[36]
    out_string = out_string + in_string[39]
    out_string = out_string + in_string[42]

    # B
    out_string = out_string + in_string[45]
    out_string = out_string + in_string[46]
    out_string = out_string + in_string[47]
    out_string = out_string + in_string[48]
    out_string = out_string + in_string[49]
    out_string = out_string + in_string[50]
    out_string = out_string + in_string[51]
    out_string = out_string + in_string[52]
    out_string = out_string + in_string[53]
    return out_string

# main
def scancubemain():

    """
    The main function: called to scan the cube

    :return: a list that shows the colour of each tiles
    """


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


    '''
    #temp: when not connected to camera, use old images
    #using opencv to load image x and y interchange!
    rgb_down = cv2.imread("down.jpg")
    rgb_side = cv2.imread("side.jpg")
    rgb_up = cv2.imread("up.jpg")
    '''

    image_number = 0
    w, h = 3, 9;
    u_yellow_rgb_values = [[0 for x in range(w)] for y in range(h)]
    w, h = 3, 9;
    r_orange_rgb_values = [[0 for x in range(w)] for y in range(h)]
    w, h = 3, 9;
    b_blue_rgb_values = [[0 for x in range(w)] for y in range(h)]
    w, h = 3, 9;
    d_white_rgb_values = [[0 for x in range(w)] for y in range(h)]
    w, h = 3, 9;
    l_red_rgb_values = [[0 for x in range(w)] for y in range(h)]
    w, h = 3, 9;
    f_green_rgb_values = [[0 for x in range(w)] for y in range(h)]


    #UP
    pix = select_pix_array('up')  # defines the array 'pix' for 'up'
    up_hsv_array = average_hsv_of_each_tile(pix, rgb_up)  # up_hsv_array contains the hsv values for
    # the yellow(u) and orange(r) sides
    u_yellow_hsv_values = up_hsv_array[:len(up_hsv_array) // 2] #getting the first 8 squares in the image
    u_yellow_hsv_values.insert(4 ,[50, 255, 255]) #insert default colour at index 4
    r_orange_hsv_values = up_hsv_array[len(up_hsv_array) // 2 :] #getting the last 8 squares in the image
    r_orange_hsv_values.insert(4 ,[5, 255, 255]) #insert default colour at index 4



    #DOWN
    pix = select_pix_array('down')  # defines the array 'pix' for 'down'
    down_hsv_array = average_hsv_of_each_tile(pix, rgb_down)  # down_rgb_array contains the rgb values for
    # the blue(b) and white(d) sides
    b_blue_hsv_values = down_hsv_array[:len(down_hsv_array) // 2]  # getting the first 8 squares in the image
    b_blue_hsv_values.insert(4, [120, 255, 10])  # insert default colour at index 4
    d_white_hsv_values = down_hsv_array[len(down_hsv_array) // 2:]  # getting the last 8 squares in the image
    d_white_hsv_values.insert(4, [0, 0, 255])  # insert default colour at index 4



    #SIDE
    pix = select_pix_array('side')  # defines the array 'pix' for 'side'
    side_hsv_array = average_hsv_of_each_tile(pix, rgb_side)  # side_rgb_array contains the rgb values for
    # the red(l) and green(f) sides
    l_red_hsv_values = side_hsv_array[:len(down_hsv_array) // 2]  # getting the first 8 squares in the image
    l_red_hsv_values.insert(4, [0, 255, 10])  # insert default colour at index 4
    f_green_hsv_values = side_hsv_array[len(down_hsv_array) // 2:]  # getting the last 8 squares in the image
    f_green_hsv_values.insert(4, [80, 255, 10])  # insert default colour at index 4

    #pprint.pprint(up_hsv_array)


    #recognising colour using function colour_reg, takes hsv value as input
    print("Start recognising colours...\n")


    output_string = colour_rec("U", u_yellow_hsv_values)   + "\n"                   #Y  #up pic upper
    output_string = output_string + colour_rec("R", r_orange_hsv_values)  + "\n"    #O  #up pic bottom
    output_string = output_string + colour_rec("F", f_green_hsv_values)   + "\n"    #G  #side pic bottom
    output_string = output_string + colour_rec("D", d_white_hsv_values)  + "\n"     #W  #down pic bottom
    output_string = output_string + colour_rec("L", l_red_hsv_values)  + "\n"       #R  #side pic upper
    output_string = output_string + colour_rec("B", b_blue_hsv_values)   + "\n"     #B  #down pic upper

    print(output_string)

    return reorder_string(formatstr(output_string))


#scancubemain()
