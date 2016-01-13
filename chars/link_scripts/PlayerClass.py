from bge import logic, types

from .PlayerStateManagement import *
from .PlayerSound import *
from .PlayerContainer import *
from .PlayerCam import *
from .PlayerFightManager import *
from .PlayerOrientation import *
from .PlayerTester import *
from .PlayerSwitchLevel import *
from .PlayerInteraction import *
from .PlayerZTargeting import *

from .Gamepad import Gamepad

scene = logic.getCurrentScene()
orientController = scene.objects['orientController']

class Player(types.KX_GameObject):

	def __init__(self, own, rig, physic, track_orient, cam):
		self.gamepad = Gamepad()
		logic.globalDict['Player']['Gamepad'] = self.gamepad
		self.rig = rig
		self.physic = physic
		self.audio = PlayerSound()
		self.tester = PlayerTester(self)
		self.fightManager = PlayerFightManager(self)
		self.interaction = PlayerInteraction()
		self.levelManager = PlayerLevelManager()
		self.orientManager = PlayerOrientationManager()
		self.camManager = PlayerCam(self, cam)
		self.heartContainer = HeartContainer(3, 3)
		self.rupeeContainer = RupeeContainer(3, 50)
		self.targetManager = PlayerZTargeting()
		self.forward_obj = None
		self.ledge_ground_obj = None
		self.detect_water_obj = None
		self.first_view_obj = None
		self.objectPickable = None

		# Container var
		self.heart = 3.0
		self.forwardForce = 0.0
		self.forwardMaxForce = 5.0
		self.fallTime = 0.0
		self.stateTime = 0.0
		self.frameCounter = 0
		self.trackTarget = None
		self.targetObject = None
		self.ledgeData = [None, None, None]
		self.ledgeGroundData = [None, None, None]
		self.ladderData = [None, None]
		self.waterPos = None

		# Tester var
		self.grounded = False
		self.onLedge = False
		self.onWater = False
		self.onLadder = False
		self.onPick = False
		self.armed = False
		self.ledgeCanceled = False
		self.trackObject = False

		# Actuator
		self.track_orientActuator = track_orient

		# get children object
		for obj in self.children:
			if (obj.name == "first_view"):
				self.first_view_obj = obj

		# Activator
		self.physic.setPlayer(self)

		# set default
		self.etat = PlayerState.IDLE_STATE
		self.etatSecondaire = -1

	def loadData(self):
		if 'heart' in logic.globalDict:
			self.heartContainer = HeartContainer(logic.globalDict['heart'], logic.globalDict['maxHeart'])

	def stopMovement(self):
		self.linearVelocity[0] = 0.0
		self.linearVelocity[1] = 0.0
		self.forwardForce = 0.0

	def getForwardForce(self):
		# if joy connected
		maxSpeed = 10.0
		speed_axis = self.gamepad.getJoyAxis1Value()
		# apply
		if (speed_axis > 0.0):
			self.forwardForce = maxSpeed * speed_axis

		if (speed_axis == 0.0):
			self.forwardForce = 0.0

		return self.forwardForce

	def linearMove(self, speed, axis, max=5.0):
		velocity = self.linearVelocity[axis]
		# positif
		if (speed > 0):
			if ( (velocity + speed) > max):
				velocity = max
			else:
				self.linearVelocity[axis] += speed
		# negatif
		else:
			if ( (velocity + speed) < max):
				velocity = max
			else:
				self.linearVelocity[axis] += speed

	def respectGroundRule(self, function):
		from link_scripts.StarterState import start_fallState

		if (self.physic.detectGround()):
			return True
		else:
			function(self)
			# go t ofall
			start_fallState(self)
			return False

	def playerHUD(self):
		return None

	def playStateTime(self, limit):
		""" Play state time with a limit
		"""
		if (self.stateTime < limit):
			self.stateTime += 0.1
		else:
			self.stateTime = limit

	def activeArmedMode(self):
		# switch weapon visibility
		self.fightManager.switchSwordAndShield()
		self.armed = True

	def switchState(self, next_etat):
		# if the next state is the idle since applic reset same var
		if (next_etat == PlayerState.IDLE_STATE):
			self.ledgeCanceled = False
		# now applic the new state
		self.etat = next_etat

	def setTrackOrient(self, target):
		if (target == None):
			self.trackTarget = None
			self.trackObject = False
		else:
			self.trackTarget = target
			self.trackObject = True

	def orient(self, cont):
		if (self.trackTarget == None):
			self.track_orientActuator.object = None
			cont.deactivate(self.track_orientActuator)
		else:
			self.track_orientActuator.object = self.trackTarget
			cont.activate(self.track_orientActuator)

	def main(self, cont):
		# update state management
		managePlayerState(self)

		# track object
		if (self.targetManager.active):
			self.targetManager.trackTargetObject(cont)
		else:
			# update axis orient
			cont.deactivate('track_orient')
			self.orientManager.updateOrientController(self.worldPosition, logic.globalDict['cam_player'].worldOrientation.to_euler())
		#self.orient(cont)

		# If touch the ground, active ground physic else fall gravity
		if (self.grounded and self.onWater == False):
			self.physic.onGround()
		else :
			if (self.onLedge == False and self.onWater == False and self.onLadder == False):
				self.physic.gravity_fall()

		# cam view
		self.camManager.cameraViewControl(self.gamepad)

		# update global dic data
		logic.globalDict['player'] = self
