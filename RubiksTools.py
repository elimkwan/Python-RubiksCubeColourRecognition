import math, kociemba, random, pycuber

def random_rubik(numMoves):
    print("Generating Random Rubik's Cube")
    faces = ["U", "R", "F", "D", "L", "B"]
    colour_moves = ["y", "o", "g", "w", "r", "b"]
    directions = ["", "'", "2"]
    sequence = Random_Moves(numMoves)
    cube = pycuber.Cube()
    cube(sequence)
    new_cube = ""
    for face in faces:
        face = cube.get_face(face)
        for x in [0,1,2]:
            for y in [0,1,2]:
                new_cube += (str(face[x][y])[1])
    relative_cube = ""
    for i in new_cube:
        relative_cube += faces[colour_moves.index(i)]
    
    return relative_cube

def Random_Moves(numMoves):
    print("Generating ", numMoves, "Random Moves")
    faces = ["U", "R", "F", "D", "L", "B"]
    directions = ["","'","2"]
    sequence = ""
    for i in range(0,17):
        sequence += faces[random.randint(0,5)]
        sequence += directions[random.randint(0,2)]
        sequence += " "
    return sequence

def Move_Translation(fileMoves):
    print("Translating Moves")
    face_reference = ["F","B","L","R","U","D"]
    newMoves = ""
    for i in range(len(fileMoves)):
        newMoves += fileMoves[i]
        if i == len(fileMoves)-1:
            print("finished translating")
        elif fileMoves[i+1] in face_reference:
            newMoves += " "
    return newMoves

def Scan_Translate(inputString):
    newString = ""
    referenceFace = {"R":"L","Y":"U","G":"F","O":"R","W":"D","B":"B"}
    for i in inputString:
        newString += referenceFace[i]
    return newString

def Scan_Translate_Backwards(inputString):
    newString = ""
    referenceFace = {"L":"R","U":"Y","F":"G","R":"O","D":"W","B":"B"}
    for i in inputString:
        newString += referenceFace[i]
    return newString

def Find_Moves(solution):
    noMoves_string=""
    move_face = []
    move_direction = []
    face_reference = ["U","R","F","D","L","B"]
    for i in range(len(solution)):
        if solution[i] in face_reference:
            move_face.append(face_reference.index(solution[i]))
            if i == len(solution)-1:
                move_direction.append(0)
        elif solution[i] == "'":
            move_direction.append(1)
        elif solution[i] == "2":
            move_face.append(move_face[-1])
            move_direction.extend([0,0])
        elif solution[i] == " " and solution[i-1] in face_reference:
            move_direction.append(0)
    print(len(move_direction), " Moves to Solve")
    return([move_direction,move_face])
