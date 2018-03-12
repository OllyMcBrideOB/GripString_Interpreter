# GripString.py


# VERSION
GRIP_STRING_VER = 0

# FINGER LABELS
NUM_FINGERS = 4
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
GRIP_END_CHAR = chr(PRINTABLE_CHAR_B2_END-1)      # set the end char to be the second to last printable char
GRIP_EMPTY_CHAR = chr(PRINTABLE_CHAR_B2_END)	  # set the end char to be the to last printable char


# CHAR LOC WITHIN STRING
GRIP_VER_LOC =       0		# location of version char
GRIP_N_FIN_LOC =     1		# location of number of fingers
GRIP_N_KFRAMES_LOC = 2	    # location of number of keyframes
GRIP_PARAMS_LOC =    3		# location of gip parameters
GRIP_END_LOC = (GRIP_PARAMS_LOC + (NUM_FINGERS * (GRIP_N_KFRAMES * 2))) 	# location of end char

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

    # print the details and position of the grip
    def printDetails(self):
        # display the number of non-empty key frames
        print("Kframes\t", end="")
        for f in range(0, NUM_FINGERS):
            print("F" + str(f) + ": " + str(self.numKeyFrames(f)) + "\t", end="")
        print("")

        # display all grip key frames. If they are empty keyframe chars, use GRIP_EMPTY_KFRAME_VAL
        for k in range(0, GRIP_N_KFRAMES):
            print("Kf[" + str(k) + "]: ", end="")
            for f in range(0, NUM_FINGERS):
                print(str(self._grip.fFrames[f].keyFrame[k].gCnt) + "," + str(self._grip.fFrames[f].keyFrame[k].fPos) + "\t", end="")
                if (self._grip.fFrames[f].keyFrame[k].gCnt < 10) or (self._grip.fFrames[f].keyFrame[k].fPos < 10):
                    print("\t", end="")     # add padding to keep columns lined up correctly
            print("")

    # return the current grip params as a grip string
    def getGripStr(self):
        gStr = ""
        gStr += self._decodeValToChar(GRIP_STRING_VER)
        gStr += self._decodeValToChar(NUM_FINGERS)
        gStr += self._decodeValToChar(GRIP_N_KFRAMES)

        # count through each finger
        for f in range(0, NUM_FINGERS):
            # convert all keyframes vals to chars. If they are empty, use empty keyframe char instead
            for k in range(0, GRIP_N_KFRAMES):
                if self._grip.fFrames[f].keyFrame[k].gCnt == GRIP_EMPTY_KFRAME_VAL:
                    gStr += GRIP_EMPTY_CHAR
                else:
                    gStr += self._decodeValToChar(self._grip.fFrames[f].keyFrame[k].gCnt)

                if self._grip.fFrames[f].keyFrame[k].fPos == GRIP_EMPTY_KFRAME_VAL:
                    gStr += GRIP_EMPTY_CHAR
                else:
                    gStr += self._decodeValToChar(self._grip.fFrames[f].keyFrame[k].fPos)

        gStr += GRIP_END_CHAR

        return gStr

    # set the grip details and positions using a grip string
    def setUsingString(self, gStr = ""):
        print("setUsingString str: " + gStr)
        # print("len: " + str(len(gStr)))

        # check the grip string version char to see if the string is compatible
        if self._decodeCharToVal(gStr[GRIP_VER_LOC]) != GRIP_STRING_VER:
            print("Grip string version incompatible.")
            print("Detected: " + self._decodeCharToVal(gStr[GRIP_VER_LOC]) + "  Expected: " + str(GRIP_STRING_VER))
            return 0

        # check the num fingers char to see if the grip string is compatible
        if self._decodeCharToVal((gStr[GRIP_N_FIN_LOC])) != NUM_FINGERS:
            print("Number of fingers in grip incompatible")
            print("Detected: " + gStr[GRIP_N_FIN_LOC] + "  Expected: " + str(NUM_FINGERS))
            return 0
        # else:
        #     print("N Fingers: " + str(self.decodeCharToValgStr[GRIP_N_FIN_LOC]))

        # check the num keyframes char to see if the grip string is compatible
        if self._decodeCharToVal((gStr[GRIP_N_KFRAMES_LOC])) != GRIP_N_KFRAMES:
            print("Number of key frames in grip incompatible")
            print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_N_KFRAMES_LOC])) + "  Expected: " + str(GRIP_N_KFRAMES))
            return 0
        # else:
        #     print("N KeyFrames: " + str(self.decodeChar(gStr[GRIP_N_KFRAMES_LOC])

        # // check the length of the string is long enough
        if len(gStr) < GRIP_END_LOC:
            print("Grip string length is too short")
            print("Detected: " + str(len(gStr)) + "  Expected: " + str(GRIP_END_LOC))
            return 0

        # // check the end char to see if the grip string is compatible
        if gStr[GRIP_END_LOC] != GRIP_END_CHAR:
            print("End char not detected")
            print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_END_LOC])) + "  Expected: " + GRIP_END_CHAR)
            return 0

        # save all grip key frames. If they are empty keyframe chars, use GRIP_EMPTY_KFRAME_VAL
        for k in range(0, GRIP_N_KFRAMES):
            for f in range(0, NUM_FINGERS):
                if gStr[GRIP_PARAMS_LOC + (k * 2)] == GRIP_EMPTY_CHAR:
                    gCnt = GRIP_EMPTY_KFRAME_VAL
                else:
                    gCnt = self._decodeCharToVal(gStr[GRIP_PARAMS_LOC + (k * 2)])

                if gStr[GRIP_PARAMS_LOC + (k * 2) + 1] == GRIP_EMPTY_CHAR:
                    fPos = GRIP_EMPTY_KFRAME_VAL
                else:
                    fPos = self._decodeCharToVal(gStr[GRIP_PARAMS_LOC + (k * 2) + 1])

                self.setKeyFrame(k, f, gCnt, fPos)

    # set the values of a keyframe. Return false if not a valid keyframe
    def setKeyFrame(self, KFn, fNum, gripCount, fPos):
        # if the keyframe number is not valid, return false
        if KFn >= GRIP_N_KFRAMES:
            print("Keyframe " + str(KFn) + " not valid")
            return 0

        if fNum >= NUM_FINGERS:
            print("Finger number " + str(fNum) + " not valid")
            return 0

        # if writing to an empty keyframe, increment number of non-empty keyframes
        if self._grip.fFrames[fNum].keyFrame[KFn].gCnt == GRIP_EMPTY_KFRAME_VAL:
            self._grip.fFrames[fNum].nKFs += 1

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



    ## DEBUGGING
    # the passed string will be deconstructed and the grip details and positions will be printed
    def printGripDetails_fromString(self, gStr =""):
        print("Grip str: " + gStr)
        print("length: " + str(len(gStr)))

        # check the grip string version char to see if the string is compatible
        if self._decodeCharToVal(gStr[GRIP_VER_LOC]) != GRIP_STRING_VER:
            print("Grip string version incompatible.")
            print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_VER_LOC])) + "  Expected: " + str(GRIP_STRING_VER))
            return 0

        # check the num fingers char to see if the grip string is compatible
        if self._decodeCharToVal(gStr[GRIP_N_FIN_LOC]) != NUM_FINGERS:
            print("Number of fingers in grip incompatible")
            print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_N_FIN_LOC])) + "  Expected: " + str(NUM_FINGERS))
            return 0
        else:
            print("N Fingers: " + str(self._decodeCharToVal(gStr[GRIP_N_FIN_LOC])))

        # check the num keyframes char to see if the grip string is compatible
        if self._decodeCharToVal(gStr[GRIP_N_KFRAMES_LOC]) != GRIP_N_KFRAMES:
            print("Number of key frames in grip incompatible")
            print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_N_KFRAMES_LOC])) + "  Expected: " + str(GRIP_N_KFRAMES))
            return 0
        else:
            print("N KeyFrames: " + str(self._decodeCharToVal(gStr[GRIP_N_KFRAMES_LOC])))

        # // check the length of the string is long enough
        if len(gStr) < GRIP_END_LOC:
            print("Grip string length is too short")
            print("Detected: " + str(len(gStr)) + "  Expected: " + str(GRIP_END_LOC))
            return 0

        # // check the end char to see if the grip string is compatible
        if gStr[GRIP_END_LOC] != GRIP_END_CHAR:
            print("End char not detected")
            print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_END_LOC])) + "  Expected: " + GRIP_END_CHAR)
            return 0

        # display the number of non-empty key frames
        print("Kframes\t", end="")
        for f in range(0,NUM_FINGERS):
            print("F" + str(f) + ": " + str(self.numKeyFrames(f)) + "\t", end="")
        print("")

        # display all grip key frames. If they are empty keyframe chars, use GRIP_EMPTY_KFRAME_VAL
        for k in range(0, GRIP_N_KFRAMES):
            print("Kf[" + str(k) + "]: ", end="")
            for f in range(0, NUM_FINGERS):
                if gStr[GRIP_PARAMS_LOC + (k * 2)] == GRIP_EMPTY_CHAR:
                    print(str(GRIP_EMPTY_KFRAME_VAL), end="")
                else:
                    print(str(self._decodeCharToVal(gStr[GRIP_PARAMS_LOC + (k * 2)])), end="")
                print(",", end="")

                if gStr[GRIP_PARAMS_LOC + (k * 2) + 1] == GRIP_EMPTY_CHAR:
                    print(str(GRIP_EMPTY_KFRAME_VAL), end="")
                else:
                    print(str(self._decodeCharToVal(gStr[GRIP_PARAMS_LOC + (k * 2) + 1])), end="")
                print("\t", end="")
            print("")
