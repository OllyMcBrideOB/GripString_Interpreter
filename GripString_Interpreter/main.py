from GripString import *
from GripPositions import *



# create a grip instance
grip = GRIP()


# # select the number of fingers and keyframes in the grip
# # grip.setNumFingers(4)
# # grip.setNumKeyframes(8)
#
# select a predefined grip
pos = predefinedPos("fist")

# save the positions in the grip
grip.setFingerPositions(pos)

# print the grip details and string
print(grip)

print("Grip String  (len: " + str(len(grip.getGripStr())) + ")\n" + grip.getGripStr())

grip.printGripDetails_fromString(grip.getGripStr())



# ## display grip strings for all predefined grips
# for x in range(0, len(defaultGripNames)):
#     pos = predefinedPos((defaultGripNames[x]))
#     grip.setFingerPositions(pos)
#     print(grip.getGripStr() + "\t" + defaultGripNames[x])










# # step through string and display values for each char
# for i in range(0, len(grip.getGripStr())):
#     print(str(i) + "(" + grip.getGripStr()[i] + ") = " + str(grip._decodeCharToVal(grip.getGripStr()[i])) + "\t", end="")
#
#     if chr(i) == GRIP_END_CHAR:
#         print("\tend char", end="")
#     elif chr(i) == GRIP_EMPTY_CHAR:
#         print("empty char", end="")
#     print("")





