from GripPositions import *


## MUST BE ANSI ENCODING
## MUST BE ANSI ENCODING
## MUST BE ANSI ENCODING
## MUST BE ANSI ENCODING

## GENERATE AND PRINT ONE DEFAULT GRIP STRING
def generateOneGripString(gripName = ""):

    # create a grip instance
    grip = GRIP()

    # select a predefined grip
    pos = predefinedPos(gripName)

    # save the positions in the grip
    grip.setFingerPositions(pos)
    grip.setName(gripName)

    # print the grip details and string
    print(grip)

    print("Grip String  (len: " + str(len(grip.getGripStr())) + ")\t" + grip.getGripStr())
    grip.setUsingString(grip.getGripStr())
    print(grip)

## GENERATE AND PRINT ALL DEFAULT GRIP STRINGS
def generateAllGripStrings(replace_w_hex = False):
    # create a grip instance
    grip = GRIP()

    # display grip strings for all predefined grips
    for x in range(0, len(defaultGripNames)):
        # get the pos values for each default grip
        pos = predefinedPos(defaultGripNames[x])

        # pass the pos and name to the GRIP
        grip.setFingerPositions(pos)
        grip.setName(defaultGripNames[x])

        # generate the grip string
        gStr = grip.getGripStr(replace_w_hex)
        gStrLen = len(gStr)

        print(f"#define DEFAULT_GRIP_{grip.getName().upper():15}{gStr}")
        
        # print the position values from the recently generated string
        # grip.decodeString_debug(grip.getGripStr())

        # clear the pos and grip values
        pos = []
        grip.clear()

### STEP THROUGH STRING AND DISPLAY VALUES FOR EACH CHAR
def printValuesOfEachChar(gStr = ""):
    # create a grip instance
    grip = GRIP()

    for i in range(0, len(grip.getGripStr())):
        print(str(i) + "(" + grip.getGripStr()[i] + ") = " + str(grip._decodeCharToVal(grip.getGripStr()[i])) + "\t", end="")

        if chr(i) == GRIP_END_CHAR:
            print("\tend char", end="")
        elif chr(i) == GRIP_EMPTY_CHAR:
            print("empty char", end="")
        print("")

### DECODE & PRINT GRIP STRING
def decodeString(gStr = ""):
    # create a grip instance
    grip = GRIP()

    grip.decodeString_debug(gStr)


## MUST BE ANSI ENCODING
## MUST BE ANSI ENCODING
## MUST BE ANSI ENCODING
## MUST BE ANSI ENCODING


####################################################################
#                       MAIN PROGRAM HERE                          #
####################################################################

# generateAllGripStrings()
generateAllGripStrings(replace_w_hex = True)
# decodeString("!%ý#!+§+$!DDD§§$!DDD§§#!!§§ýüFistüþ")
# decodeString("\x21\x25\xfd\x23\x21\x2b\xa7\x2b\x24\x21\x44\x44\x44\xa7\xa7\x24\x21\x44\x44\x44\xa7\xa7\x23\x21\x21\xa7\xa7\xfd\xfcFist\xfc\xfe")