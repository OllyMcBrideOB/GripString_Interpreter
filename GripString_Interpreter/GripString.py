# GripString.py


# VERSION
GRIP_STRING_VER = 0

# FINGER LABELS
NUM_FINGERS = 3
F0 = 0
F1 = 1
F2 = 2
F3 = 3

# KEYFRAME LABELS
GRIP_N_KFRAMES = 8
KF0 = 0
KF1 = 1
KF2 = 2
KF3 = 3
KF4 = 4
KF5 = 5
KF6 = 6
KF7 = 7

# GRIP VALUES
GRIP_EMPTY_KFRAME_VAL = 255

# PRINTABLE CHAR BLOCKS
PRINTABLE_CHAR_B1_STRT = 33     # ! start of block 1 of printable chars
PRINTABLE_CHAR_B1_END  = 126    # ~ end of block 1 of printable chars
PRINTABLE_CHAR_B2_STRT = 161    # Â¡ start of block 2 of printable chars
PRINTABLE_CHAR_B2_END  = 255    # Ã¿ end of block 2 of printable chars

# GRIP STRING CONTROL CHARS
GRIP_GR_NAME_CHAR = chr(PRINTABLE_CHAR_B2_END - 3)          # set the grip name char to be the third to last printable char
GRIP_GR_PARAMS_CHAR = chr(PRINTABLE_CHAR_B2_END - 2)        # set the grip params char to be the third to last printable char
GRIP_END_CHAR = chr(PRINTABLE_CHAR_B2_END - 1)    # set the end char to be the second to last printable char
GRIP_EMPTY_CHAR = chr(PRINTABLE_CHAR_B2_END)	  # set the empty char to be the to last printable char


# CHAR LOC WITHIN STRING
GRIP_VER_LOC       = 0		# location of version char
GRIP_N_FIN_LOC     = 1		# location of number of fingers
GRIP_N_KFRAMES_LOC = 2	    # location of number of keyframes
GRIP_PARAMS_LOC    = 3		# location of gip parameters
GRIP_END_LOC = (GRIP_PARAMS_LOC + (NUM_FINGERS * (GRIP_N_KFRAMES * 2))) 	# location of end char

# LIMITS
GRIP_NAME_MAX_LEN  = 16      # maximum length of the grip name

# individual keyframe is made up of gripCount and fingerPos
class keyFrame_t:
    def __init__(self):
       self.gCnt = GRIP_EMPTY_KFRAME_VAL
       self.fPos = GRIP_EMPTY_KFRAME_VAL

# each fingerFrame has GRIP_N_KFRAMES keyframes
class fKeyFrames_t:
    def __init__(self):
        self.nKFs = 0
        self.singlePos = 0
        self.keyFrame = [keyFrame_t()]
        for k in range(0, GRIP_N_KFRAMES):
            self.keyFrame.append(keyFrame_t())

# each grip has NUM_FINGERS fingerFrames
class gripParams_t:
    def __init__(self):
        self.fFrames = [fKeyFrames_t()]
        for k in range(0, NUM_FINGERS):
            self.fFrames.append(fKeyFrames_t())


## GRIP CLASS
class GRIP:
    def __init__(self):
        self._grip = gripParams_t()
        self._name = ""

    def __str__(self):
        self.printDetails()     # print grip details
        return ""               # return empty string as the above prints the grip details

    # def setNumFingers(self, nF):
    #     global NUM_FINGERS
    #     NUM_FINGERS = nF
    #
    # def setNumKeyframes(self, nK):
    #     global GRIP_N_KFRAMES
    #     GRIP_N_KFRAMES = nK

    # return the number of active keyframes
    def numKeyFrames(self, fNum):
        return self._grip.fFrames[fNum].nKFs

    # convert a char to a grip string value
    def _decodeCharToVal(self, char=""):
        if char == GRIP_END_CHAR:       # if the char is an end char
            return 0
        elif char == GRIP_EMPTY_CHAR:   # if the char is an empty char
            return GRIP_EMPTY_KFRAME_VAL
        elif(char >= chr(PRINTABLE_CHAR_B1_STRT)) and (char <= chr(PRINTABLE_CHAR_B1_END)):
            return ord(char) - PRINTABLE_CHAR_B1_STRT
        elif (char >= chr(PRINTABLE_CHAR_B2_STRT)) and (char <= chr(PRINTABLE_CHAR_B2_END)):
            return ord(char) - (PRINTABLE_CHAR_B2_STRT - PRINTABLE_CHAR_B1_END) - PRINTABLE_CHAR_B1_STRT

        print("Char not valid for decoding to val")
        # if the char is not within any of the printable blocks, return the 0
        return 0

    # convert a value to a grip string char
    def _decodeValToChar(self, val):
        val += PRINTABLE_CHAR_B1_STRT  # offset the value by the char offset of block 1

        # if the value is an GRIP_EMPTY_KFRAME_VAL
        if val == GRIP_EMPTY_KFRAME_VAL:
            return GRIP_EMPTY_CHAR

        # if value is within the first block
        if (val >= PRINTABLE_CHAR_B1_STRT) and (val <= PRINTABLE_CHAR_B1_END):
            return chr(val)

        val += (PRINTABLE_CHAR_B2_STRT - PRINTABLE_CHAR_B1_END)  # offset the value by the char offset of block 2

        # if value is within the first block
        if (val >= PRINTABLE_CHAR_B2_STRT) and (val <= PRINTABLE_CHAR_B2_END):
            return chr(val)

        print("Val not valid for decoding to char")
        # if the val is not within any of the printable blocks, return the end char
        return GRIP_END_CHAR

    # set the name of the grip
    def setName(self, name=""):
        self._name = name[0:GRIP_NAME_MAX_LEN]      # limit the length of the grip name
        self._name = self._name.strip()             # strip blank space

    # return the grip name
    def getName(self):
        return self._name

    # print the details and position of the grip
    def printDetails(self):
        # if there is a grip name, print it
        if (self._name):
            print(self._name + " Grip")

        # display the number of non-empty key frames
        print("Kframes\t", end="")
        for f in range(0, NUM_FINGERS):
            print("F" + str(f) + ": " + str(self.numKeyFrames(f)) + "\t", end="")
        print("")

        # calculate the maximum number of keyframes in the grip
        maxNKFrames = 0
        for f in range(0, NUM_FINGERS):
            maxNKFrames = max(self._grip.fFrames[f].nKFs, maxNKFrames)

        # display all grip key frames
        for k in range(0, maxNKFrames):
            print("Kf[" + str(k) + "]: ", end="")
            for f in range(0, NUM_FINGERS):
                if self._grip.fFrames[f].keyFrame[k].gCnt == GRIP_EMPTY_KFRAME_VAL:
                    print("\t\t\t",end="")
                else:
                    print(str(self._grip.fFrames[f].keyFrame[k].gCnt) + "," + str(self._grip.fFrames[f].keyFrame[k].fPos) + " \t", end="")
            print("")

    # return the current grip params as a grip string
    def getGripStr(self):
        gStr = ""
        gStr += self._decodeValToChar(GRIP_STRING_VER)
        gStr += self._decodeValToChar(NUM_FINGERS)

        # add opening 'grip params' special char
        gStr += GRIP_GR_PARAMS_CHAR
        # count through each finger
        for f in range(0, NUM_FINGERS):
            # add the number of keyframes to the grip string
            gStr += self._decodeValToChar(self._grip.fFrames[f].nKFs)
            # convert all keyframes vals to chars. If they are empty, use empty keyframe char instead
            for k in range(0, self._grip.fFrames[f].nKFs):
                gStr += self._decodeValToChar(self._grip.fFrames[f].keyFrame[k].gCnt)       # decode grip count to char
                gStr += self._decodeValToChar(self._grip.fFrames[f].keyFrame[k].fPos)       # decode finger pos to char
        # add closing 'grip params' special char
        gStr += GRIP_GR_PARAMS_CHAR

        # if the grip has a name
        if self._name:
            self._name = self._name.replace(' ', '_')   # replace space char with an underscore char

            # add opening 'grip name' special char
            gStr += GRIP_GR_NAME_CHAR
            gStr += self._name[0:GRIP_NAME_MAX_LEN]     # do not encode name, but limit length

            # add closing 'grip name' special char
            gStr += GRIP_GR_NAME_CHAR

        # add the string end char
        gStr += GRIP_END_CHAR

        return gStr

    # set the grip details and positions using a grip string
    def setUsingString(self, gStr = ""):
        print("setUsingString() str: " + gStr)

        ## print string and decoding
        # for i in range(0, len(gStr)):
        #     print("(" + gStr[i] + ") " + str(i) + ": " + str(self._decodeCharToVal(gStr[i])) + "\t", end="")
        #     if i == 0:
        #         print("string version", end="")
        #     elif i == 1:
        #         print("num fingers", end="")
        #
        #     if gStr[i] == GRIP_GRIP_PARAMS_CHAR:
        #         print("GRIP_GRIP_PARAMS_CHAR", end="")
        #     if gStr[i] == GRIP_END_CHAR:
        #         print("GRIP_END_CHAR", end="")
        #     if gStr[i] == GRIP_EMPTY_CHAR:
        #         print("GRIP_EMPTY_CHAR", end="")
        #     print("")


        # check the grip string version char to see if the string is compatible
        if self._decodeCharToVal(gStr[GRIP_VER_LOC]) != GRIP_STRING_VER:
            print("Grip string version incompatible.")
            print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_VER_LOC])) + "  Expected: " + str(GRIP_STRING_VER))
            return 0

        # check the num fingers char to see if the grip string is compatible
        if self._decodeCharToVal(gStr[GRIP_N_FIN_LOC]) != NUM_FINGERS:
            print("Number of fingers in grip incompatible")
            print("Detected: " + gStr[GRIP_N_FIN_LOC] + "  Expected: " + str(NUM_FINGERS))
            return 0
        else:
            print("N Fingers: " + str(self._decodeCharToVal(gStr[GRIP_N_FIN_LOC])))

        # search for grip param opening char
        gripParams = gStr.find(GRIP_GR_PARAMS_CHAR)
        # if the grip params opening char is present, decode string and store values
        if gripParams:
            # TODO add check to make sure closing char is at the expected loc
            # move to first grip param (F0 nKF)
            nKFLoc = gripParams + 1
            # count though all fingers
            for f in range(0, NUM_FINGERS):
                # count through all keyframes for this finger
                for k in range(0, self._decodeCharToVal(gStr[nKFLoc])):
                    gCnt = self._decodeCharToVal(gStr[(nKFLoc + 1) + (k * 2)])      # gCnt val is at loc (nKf + 1) + keyFrame number offset
                    fPos = self._decodeCharToVal(gStr[(nKFLoc + 2) + (k * 2)])      # fPos val is at loc (nKf + 2) + keyFrame number offset

                    self.setKeyFrame(k, f, gCnt, fPos)

                # set the new nKF location for the next finger
                nKFLoc += (self._decodeCharToVal(gStr[nKFLoc]) * 2) + 1
        else:
            print("No grip parameters detected in grip string")

        # search for grip name opening char
        gripNamesStrt = gStr.find(GRIP_GR_NAME_CHAR)
        # if the grip name opening char is present, store name
        if gripNamesStrt:
            gripNamesEnd = gStr.find(GRIP_GR_NAME_CHAR, gripNamesStrt + 1)
            self._name = gStr[gripNamesStrt + 1: gripNamesEnd]                  # store name
            self._name = self._name[0:min(len(self._name), GRIP_NAME_MAX_LEN)]  # limit name length
            self._name = self._name.replace('_', ' ')                           # replace underscore with a space char

    # set the values of a keyframe. Return false if not a valid keyframe
    def setKeyFrame(self, KFn, fNum, gripCount, fPos):
        # if the keyframe number is not valid, return false
        if KFn >= GRIP_N_KFRAMES:
            print("Keyframe " + str(KFn) + " not valid")
            return 0

        if fNum >= NUM_FINGERS:
            print("Finger number " + str(fNum) + " not valid")
            return 0

        # TODO if KF0, K! and KF3 are used, this breaks the count (as nKF == 2)
        # if writing to an empty keyframe, increment number of non-empty keyframes
        if self._grip.fFrames[fNum].keyFrame[KFn].gCnt == GRIP_EMPTY_KFRAME_VAL:
            self._grip.fFrames[fNum].nKFs += 1

        # if writing an empty val to a keyframe, decrement the number of non-empty keyframes
        if gripCount == GRIP_EMPTY_KFRAME_VAL:
            self._grip.fFrames[fNum].nKFs -= 1

        self._grip.fFrames[fNum].keyFrame[KFn].gCnt = gripCount
        self._grip.fFrames[fNum].keyFrame[KFn].fPos = fPos

        # ## TODO, this will break if the KF's are not K0 and K1
        # # if there are only 2 keyframes for this finger
        # if _grip.fFrames[fNum].nKFs == 2:
        #     # if both of those keyframes are equal				# TODO, this will break if KF1 and KF2 or more are the only KF's
        #     if (self._grip.fFrames[fNum].keyFrame[KF0].gCnt == self._grip.fFrames[fNum].keyFrame[KF1].gCnt:
        #         && (self._grip.fFrames[fNum].keyFrame[KF0].fPos == _self.grip.fFrames[fNum].keyFrame[KF1].fPos))
        #     {
        #         // set the flag to indicate that the finger only has a single pos
        #         _grip.fFrames[fNum].singlePos = true;
        #     }
        # }
        # # else if there are more/less than 2 keyframes in the grip
        # else
        # {
        #     # clear the flag
        #     _grip.fFrames[fNum].singlePos = false;
        # }

        return 1

    # set the keyframes/positions of all fingers or of a specific finger
    def setFingerPositions(self, fPositions, fNum = None):
        # # if all the positions are zero, then the array may be empty/incorrect
        # if fPositions.all() == 0:
        #     print("ERROR. positions not compatible")
        #     print(fPositions)
        #     return

        for f in range(0, len(fPositions)):
            self.setIndividualFingerPositions(f, fPositions[f])

    # set the keyframes/positions of all fingers or of a specific finger
    def setIndividualFingerPositions(self, fNum, fPositions):
        # set the keyframes/positions of an individual finger
        for KFn in range(0, len(fPositions)):
            self.setKeyFrame(KFn, fNum, fPositions[KFn][0], fPositions[KFn][1])



    # ## DEBUGGING
    # # the passed string will be deconstructed and the grip details and positions will be printed
    # def printGripDetails_fromString(self, gStr =""):
    #     print("Grip str: " + gStr)
    #     print("length: " + str(len(gStr)))
    #
    #     # check the grip string version char to see if the string is compatible
    #     if self._decodeCharToVal(gStr[GRIP_VER_LOC]) != GRIP_STRING_VER:
    #         print("Grip string version incompatible.")
    #         print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_VER_LOC])) + "  Expected: " + str(GRIP_STRING_VER))
    #         return 0
    #
    #     # check the num fingers char to see if the grip string is compatible
    #     if self._decodeCharToVal(gStr[GRIP_N_FIN_LOC]) != NUM_FINGERS:
    #         print("Number of fingers in grip incompatible")
    #         print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_N_FIN_LOC])) + "  Expected: " + str(NUM_FINGERS))
    #         return 0
    #     else:
    #         print("N Fingers: " + str(self._decodeCharToVal(gStr[GRIP_N_FIN_LOC])))
    #
    #     # check the num keyframes char to see if the grip string is compatible
    #     if self._decodeCharToVal(gStr[GRIP_N_KFRAMES_LOC]) != GRIP_N_KFRAMES:
    #         print("Number of key frames in grip incompatible")
    #         print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_N_KFRAMES_LOC])) + "  Expected: " + str(GRIP_N_KFRAMES))
    #         return 0
    #     else:
    #         print("N KeyFrames: " + str(self._decodeCharToVal(gStr[GRIP_N_KFRAMES_LOC])))
    #
    #     # // check the length of the string is long enough
    #     if len(gStr) < GRIP_END_LOC:
    #         print("Grip string length is too short")
    #         print("Detected: " + str(len(gStr)) + "  Expected: " + str(GRIP_END_LOC))
    #         return 0
    #
    #     # // check the end char to see if the grip string is compatible
    #     if gStr[GRIP_END_LOC] != GRIP_END_CHAR:
    #         print("End char not detected")
    #         print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_END_LOC])) + "  Expected: " + GRIP_END_CHAR)
    #         return 0
    #
    #     # display the number of non-empty key frames
    #     print("Kframes\t", end="")
    #     for f in range(0,NUM_FINGERS):
    #         print("F" + str(f) + ": " + str(self.numKeyFrames(f)) + "\t", end="")
    #     print("")
    #
    #     # display all grip key frames. If they are empty keyframe chars, use GRIP_EMPTY_KFRAME_VAL
    #     for k in range(0, GRIP_N_KFRAMES):
    #         print("Kf[" + str(k) + "]: ", end="")
    #         for f in range(0, NUM_FINGERS):
    #             if gStr[GRIP_PARAMS_LOC + (k * 2)] == GRIP_EMPTY_CHAR:
    #                 print(str(GRIP_EMPTY_KFRAME_VAL), end="")
    #             else:
    #                 print(str(self._decodeCharToVal(gStr[GRIP_PARAMS_LOC + (k * 2)])), end="")
    #             print(",", end="")
    #
    #             if gStr[GRIP_PARAMS_LOC + (k * 2) + 1] == GRIP_EMPTY_CHAR:
    #                 print(str(GRIP_EMPTY_KFRAME_VAL), end="")
    #             else:
    #                 print(str(self._decodeCharToVal(gStr[GRIP_PARAMS_LOC + (k * 2) + 1])), end="")
    #             print("\t", end="")
    #         print("")
