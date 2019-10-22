import math, kociemba, random, pycuber
import simpleaudio as sa
import tkinter as tk
import RubiksTools as rt
import colourRegHSV as it


"""

Running this script will run the whole program with the GUI
This script takes the array that shows the current cube state from colourRegHSV.py and generate the moves to solve the cube.
It output analogue sound waves(as stored in the audio files). 
Sound wave of different frequencies will then pass through an embedded circuit which then turn one of the 6 motors in clockwise/anticlockwise direction

DEMO: https://elimkwan.github.io/2019/08/05/cube/

"""

# Unscrambled cube UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB

AllMoves = [["Clock U.wav", "Clock R.wav", "Clock F.wav", "Clock D.wav",
             "Clock L.wav", "Clock B.wav"], ["Anti U.wav", "Anti R.wav",
                                             "Anti F.wav", "Anti D.wav", "Anti L.wav", "Anti B.wav"]]
Cube = []
global pyCube
global CurrentCube
pyCube = pycuber.Cube()
CurrentCube = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

bgColour = "white"
fgColour = "Black"

global stop
stop = False


def Solve():
    global CurrentCube
    StatusLabel.config(text="Solving Current Cube")
    root.update()
    rubiksString = CurrentCube
    moves = kociemba.solve(rubiksString)
    solution = rt.Find_Moves(moves)
    Play_Moves(solution)


def Scramble_18():
    StatusLabel.config(text="Scrambling with 18 random moves")
    root.update()
    moves = rt.Random_Moves(18)
    sequence = rt.Find_Moves(moves)
    Play_Moves(sequence)
    StatusLabel.config(text="idle")


def Scramble_From_File():
    StatusLabel.config(text="Scrambling from file")
    root.update()
    fileName = "mixup18.txt"
    file = open(fileName)
    moves = rt.Move_Translation(file.readline())
    sequence = rt.Find_Moves(moves)
    Play_Moves(sequence)
    StatusLabel.config(text="idle")


def Demo_Mode(slow):
    StatusLabel.config(text="Demo Mode")
    root.update()
    global stop
    stop = False

    while (stop == False):
        scrambleString = rt.random_rubik(18)
        scrambleMoves = rt.Find_Moves(
            kociemba.solve("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB", scrambleString))
        solveMoves = rt.Find_Moves(kociemba.solve(scrambleString))
        Moves = [scrambleMoves[0] + solveMoves[0], scrambleMoves[1] + solveMoves[1]]
        for i in range(0, len(Moves[0])):
            if stop == True:
                break;
            else:
                root.update()
                Play_Moves([[Moves[0][i]], [Moves[1][i]]])
            if slow == True:
                waveObject = sa.WaveObject.from_wave_file("Silence.wav")
                playObject = waveObject.play()
                playObject.wait_done()
    StatusLabel.config(text="idle")


def Stop_Demo():
    global stop
    stop = True


def Set_Cube():
    global CurrentCube
    CubeCoordinates = [[3, 0], [4, 0], [5, 0],
                       [3, 1], [4, 1], [5, 1],
                       [3, 2], [4, 2], [5, 2],
                       [6, 3], [7, 3], [8, 3],
                       [6, 4], [7, 4], [8, 4],
                       [6, 5], [7, 5], [8, 5],
                       [3, 3], [4, 3], [5, 3],
                       [3, 4], [4, 4], [5, 4],
                       [3, 5], [4, 5], [5, 5],
                       [3, 6], [4, 6], [5, 6],
                       [3, 7], [4, 7], [5, 7],
                       [3, 8], [4, 8], [5, 8],
                       [0, 3], [1, 3], [2, 3],
                       [0, 4], [1, 4], [2, 4],
                       [0, 5], [1, 5], [2, 5],
                       [9, 3], [10, 3], [11, 3],
                       [9, 4], [10, 4], [11, 4],
                       [9, 5], [10, 5], [11, 5]]
    for i in range(0, len(CurrentCube)):
        label = tk.Label(root, width=5, height=2,
                         relief="solid", bd=1)
        label.grid(column=(CubeCoordinates[i][0]), row=(
                CubeCoordinates[i][1] + 1))
        Cube.append(label)


def Update_Cube():
    global CurrentCube
    for i in range(0, len(Cube)):
        if CurrentCube[i] == "U":
            Cube[i].config(bg="#FEFF12")  # "#FDFEFE"
        elif CurrentCube[i] == "R":
            Cube[i].config(bg="#F5B041")  # "#F44444"
        elif CurrentCube[i] == "L":
            Cube[i].config(bg="#F44444")  # "#F5B041"
        elif CurrentCube[i] == "F":
            Cube[i].config(bg="#44F469")  # "#44F469"
        elif CurrentCube[i] == "D":
            Cube[i].config(bg="#FFFFFF")  # "#FDFEFE"
        elif CurrentCube[i] == "B":
            Cube[i].config(bg="#1251FF")  # "#1251FF"


def Update_PyCube(sequence):
    global pyCube
    faces = ["U", "R", "F", "D", "L", "B"]
    colour_moves = ["y", "o", "g", "w", "r", "b"]
    directions = ["", "'", "2"]
    letterSequence = ""

    for i in range(len(sequence[0])):
        letterSequence += faces[sequence[1][i]]
        if sequence[0][i] == 1:
            letterSequence += "'"
        letterSequence += " "

    pyCube(letterSequence)

    new_cube = ""
    for face in faces:
        face = pyCube.get_face(face)
        for x in [0, 1, 2]:
            for y in [0, 1, 2]:
                new_cube += (str(face[x][y])[1])
    relative_cube = ""
    for i in new_cube:
        relative_cube += faces[colour_moves.index(i)]
    return relative_cube


def Play_Moves(moveList):
    global CurrentCube
    print("Playing")
    move_direction = moveList[0]
    move_face = moveList[1]
    for i in range(0, len(move_face)):
        CurrentCube = Update_PyCube([[move_direction[i]], [move_face[i]]])
        Update_Cube()
        root.update()
        print(AllMoves[move_direction[i]][move_face[i]])
        waveObject = sa.WaveObject.from_wave_file(
            AllMoves[move_direction[i]][move_face[i]])
        playObject = waveObject.play()
        playObject.wait_done()
        waveObject = sa.WaveObject.from_wave_file("Silence_Norm.wav")
        playObject = waveObject.play()
        playObject.wait_done()


def Valid_String_Check(inputString):
    noU = noF = noR = noL = noB = noD = 0
    uInput = False
    for i in inputString:
        if i == "?":
            uInput = True
        elif i == "U":
            noU += 1
        elif i == "F":
            noF += 1
        elif i == "R":
            noR += 1
        elif i == "L":
            noL += 1
        elif i == "B":
            noB += 1
        elif i == "D":
            noD += 1
    if noU > 9 or noF > 9 or noR > 9 or noL > 9 or noB > 9 or noD > 9 or uInput == True:
        return False
    else:
        return True


def Scan_Cube():
    global CurrentCube
    scannedCube = it.scancubemain()
    for i in range(0, 3):
        if Valid_String_Check(scannedCube) == True:
            break
        else:
            print("Invalid Scan")
            print(CurrentCube)
            scannedCube = it.scancubemain()
    print(rt.Scan_Translate_Backwards(scannedCube))
    PyCube_Scan_Update(CurrentCube, scannedCube)
    CurrentCube = scannedCube
    Update_Cube()
    root.update()


def Manual_Cube():
    global CurrentCube
    inputString = rt.Scan_Translate(ManualInputMsg.get())
    if len(inputString) == 54:
        try:
            PyCube_Scan_Update(CurrentCube, inputString)
            CurrentCube = inputString
            print("updating colour to", inputString)
            Update_Cube()
            root.update()
        except:
            print("Invalid string input")
    else:
        print("Incorrect string length, must be 54 characters long")


def PyCube_Scan_Update(oldState, newState):
    moveList = kociemba.solve(oldState, newState)
    pyCube(moveList)


root = tk.Tk()
root.title("Rubik Solver")
root.configure(bg=bgColour)

TitleLabel = tk.Label(root, text="Rubik's Cube Solver", height=2,
                      bg=bgColour, fg=fgColour)
TitleLabel.grid(row=0, columnspan=18)

Set_Cube()
Update_Cube()

Spacer = tk.Label(root, bg=bgColour, fg=fgColour)
Spacer.grid(row=10, columnspan=12)

Scramble18Button = tk.Button(root, text="18 Random Moves", width=30,
                             command=Scramble_18,
                             bg=bgColour, fg=fgColour)
Scramble18Button.grid(row=11, column=0, columnspan=6)

FileScrambleButton = tk.Button(root, text="Scramble from file", width=30,
                               command=Scramble_From_File,
                               bg=bgColour, fg=fgColour)
FileScrambleButton.grid(row=11, column=6, columnspan=6)

DemoButton = tk.Button(root, text="Demo Mode", width=30,
                       command=lambda: Demo_Mode(False), bg=bgColour, fg=fgColour)
DemoButton.grid(row=12, column=0, columnspan=6)

SlowDemoButton = tk.Button(root, text="Slow Demo Mode", width=30,
                           command=lambda: Demo_Mode(True), bg=bgColour, fg=fgColour)
SlowDemoButton.grid(row=12, column=6, columnspan=6)

StopDemoModeButton = tk.Button(root, text="Stop Demo Mode", width=45,
                               command=Stop_Demo, bg=bgColour, fg=fgColour)
StopDemoModeButton.grid(row=13, column=0, columnspan=12)

SolveButton = tk.Button(root, text="Solve Cube", width=45, command=Solve,
                        bg=bgColour, fg=fgColour)
SolveButton.grid(row=14, column=0, columnspan=12)

DisplayLabel = tk.Label(root, text="Current Status:",
                        bg=bgColour, fg=fgColour)
DisplayLabel.grid(row=15, columnspan=12)

StatusLabel = tk.Label(root, text="idle",
                       bg=bgColour, fg=fgColour)
StatusLabel.grid(row=16, columnspan=12)

ManualControlButton = tk.Label(root, text="Manual Controls", fg=fgColour,
                               bg=bgColour)
ManualControlButton.grid(row=11, column=12, columnspan=6)

Directions = ["U", "R", "F", "D", "L", "B"]
CommandDirections = [[[0], [0]], [[0], [1]], [[0], [2]], [[0], [3]], [[0], [4]], [[0], [5]],
                     [[1], [0]], [[1], [1]], [[1], [2]], [[1], [3]], [[1], [4]], [[1], [5]]]
ManualButtons = []

for i in range(0, 6):
    MButton = tk.Button(root, text=Directions[i], width=5,
                        fg=fgColour, bg=bgColour, )
    MButton.grid(row=12, column=12 + i)
    ManualButtons.append(MButton)
for i in range(0, 6):
    MButton = tk.Button(root, text=Directions[i] + "'", width=5,
                        fg=fgColour, bg=bgColour, )
    MButton.grid(row=13, column=12 + i)
    ManualButtons.append(MButton)

# For some reason these don't work properly in a list...
ManualButtons[0].config(command=lambda: Play_Moves(CommandDirections[0]))
ManualButtons[1].config(command=lambda: Play_Moves(CommandDirections[1]))
ManualButtons[2].config(command=lambda: Play_Moves(CommandDirections[2]))
ManualButtons[3].config(command=lambda: Play_Moves(CommandDirections[3]))
ManualButtons[4].config(command=lambda: Play_Moves(CommandDirections[4]))
ManualButtons[5].config(command=lambda: Play_Moves(CommandDirections[5]))
ManualButtons[6].config(command=lambda: Play_Moves(CommandDirections[6]))
ManualButtons[7].config(command=lambda: Play_Moves(CommandDirections[7]))
ManualButtons[8].config(command=lambda: Play_Moves(CommandDirections[8]))
ManualButtons[9].config(command=lambda: Play_Moves(CommandDirections[9]))
ManualButtons[10].config(command=lambda: Play_Moves(CommandDirections[10]))
ManualButtons[11].config(command=lambda: Play_Moves(CommandDirections[11]))

ScanCubeButton = tk.Button(root, text="Scan Cube", width=20,
                           height=3, fg=fgColour, bg=bgColour,
                           command=Scan_Cube)
ScanCubeButton.grid(row=4, rowspan=3, column=13, columnspan=4)

# Manual input colour

ManualInputMsg = tk.Entry(root)
ManualInputMsg.grid(row=7, column=13, columnspan=4)
InputButton = tk.Button(root, text="Manual input colour", width=20,
                        height=3, fg=fgColour, bg=bgColour,
                        command=Manual_Cube)
InputButton.grid(row=8, rowspan=2, column=13, columnspan=4)

root.mainloop()

