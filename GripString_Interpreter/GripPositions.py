# GripPositions.py

from GripString import *    # F0, F1 etc


if NUM_FINGERS == 3:
    defaultGripNames = \
        ["Fist",
         "Hook",
         "Tripod FOP",
         "Tripod FCL",
         # "zeros"
         ]
else:
    defaultGripNames = \
        ["Fist",
         "Hook",
         "Tripod FOP",
         "Tripod FCL",
         "Pinch FOP",
         "Pinch FCL",
         # "zeros"
         ]


def predefinedPos(gripName = ""):
    # create array of positions for each finger
    pos = []
    for f in range(0, NUM_FINGERS):
        pos.append(int(0))

    gripName = gripName.lower()     # set all chars to lower case
    gripName = gripName.strip()     # remove whitespace

    if NUM_FINGERS == 3:
        if gripName == "fist":
            pos[F0] = [[0, 10],     [100, 10]]
            pos[F1] = [[0, 35],     [35, 35],   [100, 100]]
            pos[F2] = [[0, 0],      [100, 100]]

        elif gripName == "hook":
            pos[F0] = [[0, 100],     [100, 100]]
            pos[F1] = [[0, 0],       [100, 100]]
            pos[F2] = [[0, 0],       [100, 100]]

        elif gripName == "tripod fop":
            pos[F0] = [[0, 10],     [100, 10]]
            pos[F1] = [[0, 35],     [35, 35],   [100, 100]]
            pos[F2] = [[0, 100],    [100, 100]]

        elif gripName == "tripod fcl":
            pos[F0] = [[0, 10],     [100, 10]]
            pos[F1] = [[0, 35],     [35, 35],   [100, 100]]
            pos[F2] = [[0, 0],      [100, 0]]

        elif gripName == "zeros":
            zeros = []
            for k in range(0, GRIP_N_KFRAMES):
                zeros.append([0, 0])

            for f in range(0, NUM_FINGERS):
                pos[f] = zeros
        else:
            print("Grip name incorrect (" + gripName + "). Available grips: ")
            for g in range(0, len(defaultGripNames)):
                print("\t" + str(defaultGripNames[g]))

    elif NUM_FINGERS == 4:
        if gripName == "fist":
            pos[F0] = [[0, 10],     [100, 10]]
            pos[F1] = [[0, 35],     [35, 35],   [100, 100]]
            pos[F2] = [[0, 35],     [35, 35],   [100, 100]]
            pos[F3] = [[0, 0],      [100, 100]]

        elif gripName == "hook":
            pos[F0] = [[0, 100],    [100, 100]]
            pos[F1] = [[0, 0],      [100, 100]]
            pos[F2] = [[0, 0],      [100, 100]]
            pos[F3] = [[0, 0],      [100, 100]]

        elif gripName == "tripod fop":
            pos[F0] = [[0, 3],      [100, 3]]
            pos[F1] = [[0, 35],     [35, 35],    [100, 100]]
            pos[F2] = [[0, 35],     [35, 35],    [100, 100]]
            pos[F3] = [[0, 100],    [100, 100]]

        elif gripName == "tripod fcl":
            pos[F0] = [[0, 3],      [100, 3]]
            pos[F1] = [[0, 35],     [35, 35],    [100, 100]]
            pos[F2] = [[0, 35],     [35, 35],    [100, 100]]
            pos[F3] = [[0, 0],      [100, 0]]

        elif gripName == "pinch fop":
            pos[F0] = [[0, 12],     [100, 12]]
            pos[F1] = [[0, 22],     [22, 22],    [100, 100]]
            pos[F2] = [[0, 100],    [100, 100]]
            pos[F3] = [[0, 100],    [100, 0]]

        elif gripName == "pinch fcl":
            pos[F0] = [[0, 12],     [100, 12]]
            pos[F1] = [[0, 22],     [22, 22],   [100, 100]]
            pos[F2] = [[0, 100],    [100, 0]]
            pos[F3] = [[0, 100],    [100, 0]]

        elif gripName == "zeros":
            zeros = []
            for k in range(0, GRIP_N_KFRAMES):
                zeros.append([0, 0])

            for f in range(0, NUM_FINGERS):
                pos[f] = zeros

        else:
            print("Grip name incorrect. Available grips: ")
            for g in range(0, len(defaultGripNames)):
                print("\t" + str(defaultGripNames[g]))

    else:
        print("ERROR, number of fingers not compatible (" + str(NUM_FINGERS))

    return pos




