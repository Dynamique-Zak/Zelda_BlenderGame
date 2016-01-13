from bge import logic, events
import pygame

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED
ACTIVE = logic.KX_INPUT_ACTIVE

class Gamepad:

	def __init__(self):
		self.keyboard = logic.keyboard
		self.joystick = None
		self.up = events.UPARROWKEY
		self.left = events.LEFTARROWKEY
		self.down = events.DOWNARROWKEY
		self.right = events.RIGHTARROWKEY
		self.action = events.XKEY
		self.attack = events.CKEY
		# items keys
		self.itemX = events.QKEY
		self.itemY = events.SKEY
		#
		self.look = events.SKEY
		self.target = events.WKEY

		# init joy
		self.initJoystick()

	# * Joystick part
	def initJoystick(self):
		pygame.joystick.init() #initialize joystick module
		pygame.joystick.get_init() #verify initialization (boolean)

		self.joystick = pygame.joystick.Joystick(0)
		print("Joystick ", self.joystick.get_name(), " is connected")
		self.joystick.init()
		self.joystick.get_init()

	def joystickConnected(self):
		if (self.joystick != None):
			return True
		else:
			return False

	def joyAxisActive(self):
		axis = self.getJoyAxis1()
		for val in axis:
			if (axis != 0.0):
				return True
		return False

	def getJoyAxis1(self):
		Joy1Xaxis = self.joystick.get_axis(0)
		Joy1Yaxis = self.joystick.get_axis(1)
		# Joy1Xaxis2 = self.joystick.get_axis(2)
		# Joy1Yaxis2 = self.joystick.get_axis(3)
		return [Joy1Xaxis, Joy1Yaxis]

	def getJoyAxis1Value(self):
		axis = self.getJoyAxis1()
		value = axis[0]
		if (axis[1] != 0.0):
			value = axis[1]
		return value

	# * Moved keys
	def isUpPressed(self, state=ACTIVE):
		toUp = False
		axis = self.getJoyAxis1()[1]
		if (self.keyboard.events[self.up] == state):
			toUp = True
		elif axis < 0:
			toUp = True
		return toUp

	def isDownPressed(self, state=ACTIVE):
		toDown = False
		axis = self.getJoyAxis1()[1]
		if (self.keyboard.events[self.down] == state):
			toDown = True
		elif axis > 0.1:
			toDown = True
		return toDown

	def isLeftPressed(self, state=ACTIVE):
		toLeft = False
		axis = self.getJoyAxis1()[0]
		if (self.keyboard.events[self.left] == state):
			toLeft = True
		elif (axis < 0):
			toLeft = True
		return toLeft

	def isRightPressed(self, state=ACTIVE):
		toRight = False
		axis = self.getJoyAxis1()[0]
		if (self.keyboard.events[self.right] == state):
			toRight = True
		elif (axis > 0):
			toRight = True
		return toRight

	# * Special keys
	def isActionPressed(self):
		check = False
		if (self.keyboard.events[self.action] == ACTIVE):
			check = True
		elif (self.joystick.get_button(3)):
			check = True
		return check

	def isAttackPressed(self):
		check = False
		if (self.keyboard.events[self.attack] == ACTIVE):
			check = True
		elif (self.joystick.get_button(2)):
			check = True
		return check

	def isLookPressed(self):
		if (self.keyboard.events[self.look] == ACTIVE): return True
		return False

	# * Items key
	def isItemXPressed(self, state=JUST_ACTIVATED):
		check = False
		if (self.keyboard.events[self.itemX] == state):
			check = True
		elif (self.joystick.get_button(0)):
			check = True
		return check

	def isItemYPressed(self, state=JUST_ACTIVATED):
		check = False
		if (self.keyboard.events[self.itemY] == state):
			check = True
		elif (self.joystick.get_button(1)):
			check = True
		return check

	# * Tester
	def isArrowPressed(self):
		# joystick part
		#axis = self.joystick.axis
		# keyboard
		event = self.keyboard.events
		if ( event[self.up] == ACTIVE or event[self.down] == ACTIVE or event[self.left] == ACTIVE or event[self.right] == ACTIVE ):
			return True
		else :
			return False
