from bge import logic, events

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
ACTIVE = logic.KX_INPUT_ACTIVE

Z = 7

class KeyboardController:
	"""
	Keyboard Controller
	Can simule axis joy value for play with a keyboard
	"""
	def __init__(self):
		self.keyboard = logic.keyboard
		self.up = events.UPARROWKEY
		self.left = events.LEFTARROWKEY
		self.down = events.DOWNARROWKEY
		self.right = events.RIGHTARROWKEY
		self.action = events.XKEY
		self.attack = events.CKEY
		# *
		self.attack = events.CKEY
		# items keys
		self.itemX = events.QKEY
		self.itemY = events.SKEY
		#
		self.look = events.SKEY
		self.target = events.WKEY
		self.pause = events.AKEY
		# value smiluation
		self.axis1 = [0.0, 0.0]
		self.sensibility = 0.1

	def addAxis1Value(self, index, speed):
		nextVal = (self.axis1[index] + speed)
		# test reset
		if ( (speed < 0.0 and self.axis1[index] > 0.0) or (speed > 0.0 and self.axis1[index] < 0.0) ):
			self.axis1[index] = 0.0

		# other
		if ( (speed > 0.0 and nextVal < 1.0) or (speed < 0.0 and nextVal > -1.0) ):
			self.axis1[index] += speed
		else:
			if (speed > 0.0):
				self.axis1[index] = 1.0
			else:
				self.axis1[index] = -1.0

	def simuleJoyAxis(self):
		"""
		Get joy axis keyboard version
		"""
		# Simule UpDown axis joystick with keyboard
		if (self.keyboard.events[self.up] == ACTIVE):
			self.addAxis1Value(1, -self.sensibility)

		elif (self.keyboard.events[self.down] == ACTIVE):
			self.addAxis1Value(1, self.sensibility)
		else:
			self.axis1[1] = 0.0

		# Simule LeftRight axis joystick with keyboard
		if (self.keyboard.events[self.left] == ACTIVE):
			self.addAxis1Value(0, -self.sensibility)

		elif (self.keyboard.events[self.right] == ACTIVE):
			self.addAxis1Value(0, self.sensibility)
		else:
			self.axis1[0] = 0.0

		return self.axis1

	def simuleJoyAxisValue(self):
		"""
		Get joy axis value keyboard version
		"""
		axis = self.simuleJoyAxis()
		value = 0.0
		x_axis = abs(axis[0])
		y_axis = abs(axis[1])

		if ( x_axis > y_axis):
			value = x_axis
		elif( y_axis > x_axis):
			value = y_axis
		elif (y_axis != 0.0 and x_axis != 0.0):
			value = (y_axis + x_axis) / 2

		return value

class Gamepad:

	def __init__(self):

		self.joystick = None
		self.keyboardController = KeyboardController()
		self.lastButton = None
		# init joy
		self.initJoystick()

	# =================================================================
	# * Joystick part
	# =================================================================
	def initJoystick(self):
		# If joystick is activate in configuration
		if (logic.globalDict['CONFIGURATION']['useJoystick'] == 1):
			# Import pygame
			import pygame

			# Init
			pygame.display.init() # Init pygame display for event
			pygame.joystick.init() # Initialize joystick module
			pygame.joystick.get_init() # Verify initialization (boolean)

			if ( pygame.joystick.get_count() > 0 ):
				self.joystick = pygame.joystick.Joystick(0)
				self.joystick.init()
				self.joystick.get_init()
				print("Joystick ", self.joystick.get_name(), " is connected")

	def joystickConnected(self):
		if (self.joystick != None):
			return True
		else:
			return False

	def updateJoystick(self):
		if ( self.joystickConnected() ):
			pygame.event.pump()

	def joyAxisActive(self):
		axis = self.getJoyAxis1()
		for val in axis:
			if (axis != 0.0):
				return True
		return False

	def getJoyButton(self, indexButton):
		check = False
		if ( self.joystickConnected() ):
			if ( self.joystick.get_button(indexButton) ):
				check = True
		return check

	def getJoyAxis1(self):
		Joy1Xaxis = 0.0
		Joy1Yaxis = 0.0
		# If joystick connected
		if (self.joystickConnected()):
			Joy1Xaxis = self.joystick.get_axis(0)
			Joy1Yaxis = self.joystick.get_axis(1)

		if (Joy1Xaxis == 0.0 and Joy1Yaxis == 0.0 ):
			Joy1Xaxis = self.keyboardController.simuleJoyAxis()[0]
			Joy1Yaxis = self.keyboardController.simuleJoyAxis()[1]
		# Joy1Xaxis2 = self.joystick.get_axis(2)
		# Joy1Yaxis2 = self.joystick.get_axis(3)
		return [Joy1Xaxis, Joy1Yaxis]

	def getJoyAxis2(self):
		Joy2Xaxis = 0.0
		Joy2Yaxis = 0.0
		if ( self.joystickConnected() ):
			Joy2Xaxis = self.joystick.get_axis(2)
			Joy2Yaxis = self.joystick.get_axis(3)
		# Joy1Xaxis2 = self.joystick.get_axis(2)
		# Joy1Yaxis2 = self.joystick.get_axis(3)
		return [Joy2Xaxis, Joy2Yaxis]

	def getJoyAxis1Value(self):
		axis = self.getJoyAxis1()
		value = 0.0
		x_axis = abs(axis[0])
		y_axis = abs(axis[1])

		if ( x_axis > y_axis):
			value = x_axis
		elif( y_axis > x_axis):
			value = y_axis
		elif (y_axis != 0.0 and x_axis != 0.0):
			value = (y_axis + x_axis) / 2

		return value

	# =================================================================
	# * Moved keys
	# =================================================================
	def isUpPressed(self, state=ACTIVE):
		toUp = False
		axis = self.getJoyAxis1()[1]
		if (self.keyboardController.keyboard.events[self.keyboardController.up] == state):
			toUp = True
		elif axis < 0:
			toUp = True
		return toUp

	def isDownPressed(self, state=ACTIVE):
		toDown = False
		axis = self.getJoyAxis1()[1]
		if (self.keyboardController.keyboard.events[self.keyboardController.down] == state):
			toDown = True
		elif axis > 0.1:
			toDown = True
		return toDown

	def isLeftPressed(self, state=ACTIVE):
		toLeft = False
		axis = self.getJoyAxis1()[0]
		if (self.keyboardController.keyboard.events[self.keyboardController.left] == state):
			toLeft = True
		# elif (axis < 0):
		# 	toLeft = True
		return toLeft

	def isRightPressed(self, state=ACTIVE):
		toRight = False
		axis = self.getJoyAxis1()[0]
		if (self.keyboardController.keyboard.events[self.keyboardController.right] == state):
			toRight = True
		# elif (axis > 0):
		# 	toRight = True
		return toRight

	# * Special keys
	def isActionPressed(self, state=ACTIVE):
		check = False
		if (self.keyboardController.keyboard.events[self.keyboardController.action] == state):
			check = True
		elif (self.getJoyButton(3)):
			check = True
		return check

	def isAttackPressed(self, state=ACTIVE):
		check = False
		if (self.keyboardController.keyboard.events[self.keyboardController.attack] == state):
			check = True
		elif (self.getJoyButton(2)):
			check = True
		return check

	def isLookPressed(self):
		if (self.keyboardController.keyboard.events[self.keyboardController.look] == ACTIVE): return True
		return False

	def isZPressed(self, state=ACTIVE):
		check = False
		if (self.keyboardController.keyboard.events[self.keyboardController.target] == state):
			check = True
		if (self.getJoyButton(Z) ):
			check = True
		return check

	# * Items key
	def isItemXPressed(self, state=JUST_ACTIVATED):
		check = False
		if (self.keyboardController.keyboard.events[self.keyboardController.itemX] == state):
			check = True
		elif (self.getJoyButton(0)):
			check = True
		return check

	def isItemYPressed(self, state=JUST_ACTIVATED):
		check = False
		if (self.keyboardController.keyboard.events[self.keyboardController.itemY] == state):
			check = True
		elif (self.getJoyButton(1)):
			check = True
		return check

	def isPausePressed(self, state=JUST_ACTIVATED):
		check = False
		if (self.keyboardController.keyboard.events[self.keyboardController.pause] == state):
			check = True
		elif (self.getJoyButton(1)):
			check = True
		return check

	# * Tester
	def isArrowPressed(self):
		# joystick part
		#axis = self.joystick.axis
		# keyboard
		event = self.keyboardController.keyboard.events
		if ( event[self.keyboardController.up] == ACTIVE or event[self.keyboardController.down] == ACTIVE or event[self.keyboardController.left] == ACTIVE or event[self.keyboardController.right] == ACTIVE ):
			return True
		else :
			return False
