# GripString.py


# Grip string format (Ver 0, 13/03/18)
#
# 	V F gpc gripParams gpc gnc gripName gnc endc
#
# 	V			- version of grip string
# 	F			- number of fingers
# 	gpc			- grip parameter control char
# 	gripParams	- grip keyframes for each finger ({F0_nKFs, {gCnt, fPos}, {gCnt, fPos}}, {F1_nKFs, {gCnt, fPos} ...)
# 	gnc			- grip name control char
# 	gripName	- name of the grip (not encoded, limited to GRIP_NAME_MAX_LEN)
# 	endc		- end char (char 254)
#
# 	The grip values are encoded from uint8_t vals to ASCII (and exteneded ASCII) chars
# 	which have been tested to be printable over common serial terminals.
# 	The ASCII set is split into 2 blocks (33 - 126, 161 - 255) of printable chars, and
# 	are used to represent either a decimal value (33 = 0, 34 = 1 etc) or a control
# 	char (255 = empty value, 254 = endc etc).
# #

# VERSION
GRIP_STRING_VER = 0

# LIMITS
GRIP_NAME_MAX_LEN  = 16      # maximum length of the grip name

# GRIP VALUES
GRIP_EMPTY_KFRAME_VAL = 255

# FINGER LABELS
# NUM_FINGERS = 4
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

# PRINTABLE CHAR BLOCKS
PRINTABLE_CHAR_B1_STRT = 33     # ! start of block 1 of printable chars
PRINTABLE_CHAR_B1_END  = 126    # ~ end of block 1 of printable chars
PRINTABLE_CHAR_B2_STRT = 161    # Â¡ start of block 2 of printable chars
PRINTABLE_CHAR_B2_END  = 255    # Ã¿ end of block 2 of printable chars

# GRIP STRING CONTROL CHARS
GRIP_GR_NAME_INT = (PRINTABLE_CHAR_B2_END - 3)      # set the grip name char to be the fourth to last printable char
GRIP_GR_PARAMS_INT = (PRINTABLE_CHAR_B2_END - 2)    # set the grip params char to be the third to last printable char
GRIP_END_INT = (PRINTABLE_CHAR_B2_END - 1)          # set the end char to be the second to last printable char
GRIP_EMPTY_INT = (PRINTABLE_CHAR_B2_END)	        # set the empty char to be the to last printable char

GRIP_GR_NAME_CHAR = chr(GRIP_GR_NAME_INT)           # set the grip name char to be the fourth to last printable char
GRIP_GR_PARAMS_CHAR = chr(GRIP_GR_PARAMS_INT)       # set the grip params char to be the third to last printable char
GRIP_END_CHAR = chr(GRIP_END_INT)                   # set the end char to be the second to last printable char
GRIP_EMPTY_CHAR = chr(GRIP_EMPTY_INT)	            # set the empty char to be the to last printable char


# CHAR LOC WITHIN STRING
GRIP_VER_LOC       = 0		# location of version char
GRIP_N_FIN_LOC     = 1		# location of number of fingers
GRIP_PARAMS_LOC    = 2		# location of gip parameters
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
		self.fFrame = [fKeyFrames_t()]
		for k in range(0, NUM_FINGERS):
			self.fFrame.append(fKeyFrames_t())


## GRIP CLASS
class GRIP:
	def __init__(self):
		self._grip = gripParams_t()
		self._name = ""

	def __str__(self):
		self.printDetails()     # print grip details
		return ""               # return empty string as the above prints the grip details

	# return the number of active keyframes
	def numKeyFrames(self, fNum):
		return self._grip.fFrame[fNum].nKFs

	# convert a char to a grip string value
	def _decodeCharToVal(self, char=""):
		if char == GRIP_END_CHAR:       # if the char is an end char
			return 0
		elif char == GRIP_EMPTY_CHAR:   # if the char is an empty char
			return GRIP_EMPTY_KFRAME_VAL
		elif(char >= chr(PRINTABLE_CHAR_B1_STRT)) and (char <= chr(PRINTABLE_CHAR_B1_END)):
			return ord(char) - PRINTABLE_CHAR_B1_STRT
		elif (char >= chr(PRINTABLE_CHAR_B2_STRT)) and (char <= chr(PRINTABLE_CHAR_B2_END)):
			return ord(char) - ( ( PRINTABLE_CHAR_B2_STRT - PRINTABLE_CHAR_B1_END ) - 1) - PRINTABLE_CHAR_B1_STRT

		print("Char not valid for decoding to val (" + str(ord(char)) + ")")
		# if the char is not within any of the printable blocks, return the 0
		return 0

	# convert a value to a grip string char
	def _decodeValToChar(self, val):
		# if the value is an GRIP_EMPTY_KFRAME_VAL
		if val == GRIP_EMPTY_KFRAME_VAL:
			return chr(GRIP_EMPTY_CHAR)

		val += PRINTABLE_CHAR_B1_STRT  # offset the value by the char offset of block 1

		# if value is within the first block
		if (val >= PRINTABLE_CHAR_B1_STRT) and (val <= PRINTABLE_CHAR_B1_END):
			return chr(val)

		val += (PRINTABLE_CHAR_B2_STRT - PRINTABLE_CHAR_B1_END) - 1  # offset the value by gap size between blocks 1 and 2

		# if value is within the second block
		if (val >= PRINTABLE_CHAR_B2_STRT) and (val <= PRINTABLE_CHAR_B2_END):
			return chr(val)
		else:
			# if the val is not within any of the printable blocks, return the end char
			print("Val not valid for decoding to char")
			return chr(GRIP_END_CHAR)

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
		maxnKFs = 0
		for f in range(0, NUM_FINGERS):
			maxnKFs = max(self._grip.fFrame[f].nKFs, maxnKFs)

		# display all grip key frames
		for k in range(0, maxnKFs):
			print("Kf[" + str(k) + "]: ", end="")
			for f in range(0, NUM_FINGERS):
				if self._grip.fFrame[f].keyFrame[k].gCnt == GRIP_EMPTY_KFRAME_VAL:
					print("\t\t\t",end="")
				else:
					print(str(self._grip.fFrame[f].keyFrame[k].gCnt) + "," + str(self._grip.fFrame[f].keyFrame[k].fPos) + " \t", end="")
			print("")

	# either return 'c' as a char, or convert it into a hex-string value (e.g. '\x<val>')
	def _encodeAsHex(self, c, replace_w_hex):
		if replace_w_hex:
			return "\\x" + str(hex(ord(c))[2:])
		else:
			return str(c)

	# return the current grip params as a grip string
	def getGripStr(self, replace_w_hex = False):
		gStr = "\""

		# add opening 'grip params' special char
		gStr += self._encodeAsHex(self._decodeValToChar(GRIP_STRING_VER), replace_w_hex)
		gStr += self._encodeAsHex(self._decodeValToChar(NUM_FINGERS), replace_w_hex)
		gStr += self._encodeAsHex(GRIP_GR_PARAMS_CHAR, replace_w_hex)

		# count through each finger
		for f in range(0, NUM_FINGERS):
			# add the number of keyframes to the grip string
			gStr += self._encodeAsHex(self._decodeValToChar(self._grip.fFrame[f].nKFs), replace_w_hex)
			# convert all keyframes vals to chars. If they are empty, use empty keyframe char instead
			for k in range(0, self._grip.fFrame[f].nKFs):
				gStr += self._encodeAsHex(self._decodeValToChar(self._grip.fFrame[f].keyFrame[k].gCnt), replace_w_hex)       # decode grip count to char
				gStr += self._encodeAsHex(self._decodeValToChar(self._grip.fFrame[f].keyFrame[k].fPos), replace_w_hex)       # decode finger pos to char
		# add closing 'grip params' special char
		gStr += self._encodeAsHex(GRIP_GR_PARAMS_CHAR, replace_w_hex)

		# if the grip has a name
		if self._name:
			self._name = self._name.replace(' ', '_')   # replace space char with an underscore char

			# add opening 'grip name' special char
			gStr += self._encodeAsHex(GRIP_GR_NAME_CHAR, replace_w_hex)
				
			# add the grip name (ensure the name is surrounded by it's own speech marks to prevent it getting absorbed by the previous `\x` str)
			gStr += "\" \"" + self._name[0:GRIP_NAME_MAX_LEN] + "\" \""     # do not encode name, but limit length

			# add closing 'grip name' special char
			gStr += self._encodeAsHex(GRIP_GR_NAME_CHAR, replace_w_hex)

		# add the string end char
		gStr += self._encodeAsHex(GRIP_END_CHAR, replace_w_hex) + "\""

		return gStr

	# set the grip details and positions using a grip string
	def setUsingString(self, gStr = ""):
		print("setUsingString() str: " + gStr)

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
			# move to first grip param after grip param opening char (F0 nKF)
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

	# clear the current grip
	def clear(self):
		self.setName("")

		for f in range(0, NUM_FINGERS):
			self._grip.fFrame[f].nKFs = 0

			for k in range(0, GRIP_N_KFRAMES):
				self._grip.fFrame[f].keyFrame[k].gCnt = GRIP_EMPTY_KFRAME_VAL
				self._grip.fFrame[f].keyFrame[k].fPos = GRIP_EMPTY_KFRAME_VAL

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

	# set the values of a keyframe. Return false if not a valid keyframe
	def setKeyFrame(self, KFn, fNum, gripCount, fPos):
		# if the keyframe number is not valid, return false
		if KFn >= GRIP_N_KFRAMES:
			print("Keyframe " + str(KFn) + " not valid")
			return 0

		if fNum >= NUM_FINGERS:
			print("Finger number " + str(fNum) + " not valid")
			return 0

		# TODO if KF0 and KF3 are used, this breaks the count (as nKF == 2)
		# if writing to an empty keyframe, increment number of non-empty keyframes
		if self._grip.fFrame[fNum].keyFrame[KFn].gCnt == GRIP_EMPTY_KFRAME_VAL:
			self._grip.fFrame[fNum].nKFs += 1

		# if writing an empty val to a keyframe, decrement the number of non-empty keyframes
		if gripCount == GRIP_EMPTY_KFRAME_VAL:
			self._grip.fFrame[fNum].nKFs -= 1

		self._grip.fFrame[fNum].keyFrame[KFn].gCnt = gripCount
		self._grip.fFrame[fNum].keyFrame[KFn].fPos = fPos

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

	## DEBUGGING
	# the passed string will be deconstructed and the grip details and positions will be printed
	def decodeString_debug(self, gStr =""):
		print("Grip str: " + gStr)
		print("Str length: " + str(len(gStr)))

		# check the grip string version char to see if the string is compatible
		if self._decodeCharToVal(gStr[GRIP_VER_LOC]) != GRIP_STRING_VER:
			print("Grip string version incompatible.")
			print("Detected: " + str(self._decodeCharToVal(gStr[GRIP_VER_LOC])) + "  Expected: " + str(GRIP_STRING_VER))
			return 0

		print("G Str version: " + str(self._decodeCharToVal(gStr[GRIP_VER_LOC])))


		# check the num fingers char to see if the grip string is compatible
		if self._decodeCharToVal(gStr[GRIP_N_FIN_LOC]) != NUM_FINGERS:
			print("Number of fingers in grip incompatible")
			print("Detected: " + gStr[GRIP_N_FIN_LOC] + "  Expected: " + str(NUM_FINGERS))
			return 0
		else:
			print("N Fingers: " + str(self._decodeCharToVal(gStr[GRIP_N_FIN_LOC])))


		# search for grip name opening char
		gripNamesStrt = gStr.find(GRIP_GR_NAME_CHAR)
		# if the grip name opening char is present, store name
		if gripNamesStrt:
			gripNamesEnd = gStr.find(GRIP_GR_NAME_CHAR, gripNamesStrt + 1)
			print("Name: " + gStr[gripNamesStrt + 1: gripNamesEnd])

		# search for grip param opening char
		gripParams = gStr.find(GRIP_GR_PARAMS_CHAR)
		# if the grip params opening char is present, decode string and store values
		if gripParams:
			# TODO add check to make sure closing char is at the expected loc
			# move to first grip param after grip param opening char (F0 nKF)
			nKFLoc = []
			for i in range(0, NUM_FINGERS):
				nKFLoc.append(0)

			nKFLoc[0] = gripParams + 1
			maxnKFs = 0
			print("nKFs:\t", end="")
			# count though all fingers
			for f in range(0, NUM_FINGERS):
				# print finger number and number of keyframes
				print("F" + str(f) + ": " + str(self._decodeCharToVal(gStr[nKFLoc[f]])) , end="")

				# if there are only 2 keyframes, check for singlePos
				if self._decodeCharToVal(gStr[nKFLoc[f]]) == 2:
					if self._decodeCharToVal(gStr[(nKFLoc[f] + 2) + (KF0 * 2)]) == self._decodeCharToVal(gStr[(nKFLoc[f] + 2) + (KF1 * 2)]):
						print("*", end="")

				print("\t", end="")

				# calculate the maxnKFs for this grip
				maxnKFs = max(self._decodeCharToVal(gStr[nKFLoc[f]]), maxnKFs)

				# move to the next nKFLoc
				if f < NUM_FINGERS - 1:
					nKFLoc[f + 1] = nKFLoc[f] + (self._decodeCharToVal(gStr[nKFLoc[f]]) * 2) + 1

			print("")

			# count through all keyframes for this grip
			for k in range(0, maxnKFs):
				print("Kf[" + str(k) + "]\t", end="")
				# count though all fingers
				for f in range(0, NUM_FINGERS):
					if k < self._decodeCharToVal(gStr[nKFLoc[f]]):
						print(str(self._decodeCharToVal(gStr[(nKFLoc[f] + 1) + (k * 2)])) + "," + str(self._decodeCharToVal(gStr[(nKFLoc[f] + 2) + (k * 2)])) + "\t", end="")

						# sort padding
						if self._decodeCharToVal(gStr[(nKFLoc[f] + 1) + (k * 2)]) < 10 and self._decodeCharToVal(gStr[(nKFLoc[f] + 2) + (k * 2)]) < 10:
							print("\t", end="")
					else:
						print("\t\t", end="")
				print("")

		else:
			print("No grip parameters detected in grip string")
