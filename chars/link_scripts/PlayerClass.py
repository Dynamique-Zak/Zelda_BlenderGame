from bge import logic, types
# * Imports
from .PlayerStateManagement import *
from .PlayerSound import *
from .SwordTrail import *
from .PlayerContainer import *
from .PlayerCam import *
from .PlayerFightManager import *
from .PlayerPickManager import *
from .PlayerObjectManager import *
from .PlayerOrientation import *
from .PlayerTester import *
from .PlayerSwitchLevel import *
from .PlayerInteraction import *
from link_scripts.PlayerInventory import *
from .PlayerZTargeting import *

from .Gamepad import Gamepad

scene = logic.getCurrentScene()
orientController = scene.objects['orientController']

class Player(types.KX_GameObject):

	def __init__(self, own, rig, physic, track_orient, cam):
		# Init Player
		self.gamepad = Gamepad()
		logic.globalDict['Player']['Gamepad'] = self.gamepad
		self.rig = rig
		self.physic = physic
		self.audio = PlayerSound()
		self.swordTrail = SwordTrail()
		self.tester = PlayerTester(self)
		self.objectManager = PlayerObjectManager(self)
		self.fightManager = PlayerFightManager(self)
		self.pickManager = PlayerPickManager(self)
		self.inventory = PlayerInventory(self)
		self.interaction = PlayerInteraction()
		self.levelManager = PlayerLevelManager()
		self.orientManager = PlayerOrientationManager()
		self.camManager = PlayerCam(self, cam)
		self.heartContainer = HeartContainer(3, 3)
		self.rupeeContainer = RupeeContainer(0, 50)
		self.targetManager = PlayerZTargeting()
		self.forward_obj = None
		self.ledge_ground_obj = None
		self.detect_water_obj = None
		self.first_view_obj = None

		# Container var
		self.heart = 3.0
		self.forwardForce = 0.0
		self.forwardMaxForce = 5.0
		self.fallTime = 0.0
		self.stateTime = 0.0
		self.frameCounter = 0
		self.shufferedDamage = 0.0
		self.comboAttack = 0
		self.trackTarget = None
		self.targetObject = None
		self.targetObjectData = [None, None]
		self.lastGroundPos = [0, 0, 0]
		self.ledgeData = [None, None, None]
		self.ledgeGroundData = [None, None, None]
		self.ladderData = [None, None]
		self.waterPos = None

		# Tester var
		self.grounded = False
		self.onLedge = False
		self.onWater = False
		self.onLadder = False
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
		# If player global dict exist
		if 'Player' in logic.globalDict:
			if 'heart' in logic.globalDict['Player']['heartContainer']:
				heartContainer = logic.globalDict['Player']['heartContainer']
				self.heartContainer.load(heartContainer['heart'], heartContainer['maxHeart'])

	def stopMovement(self):
		self.linearVelocity[0] = 0.0
		self.linearVelocity[1] = 0.0
		self.forwardForce = 0.0

	def cancelAttack(self):
		self.swordTrail.deactiveTrail()
		# reset combo
		self.comboAttack = 0
		# reset damage
		setDamage(0)

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

	def respectGroundRule(self, function, goToFall=True):
		from link_scripts.StarterState import start_fallState

		if (self.tester.detectGround()):
			return True
		else:
			if (function != None):
				function(self)
			# go tofall
			if (goToFall):
				start_fallState(self)
			return False

	def isAlive(self):
		return ( not self.heartContainer.notHaveHeart() )

	def applyDamage(self):
		damage = self.shufferedDamage
		self.heartContainer.loseHeart(damage)

	def alignToTargetObject(self):
		# If have interaction pos
		have_i_pos = False
		new_pos = [0, 0, 0]
		orient = None
		for obj in self.targetObject.children:
			if "i_pos" in obj.name :
				new_pos[0] = obj.worldPosition[0]
				new_pos[1] = obj.worldPosition[1]
				orient = obj.worldOrientation.to_euler()
				have_i_pos = True
		# If find interaction pos apply
		if (have_i_pos):
			self.worldOrientation = orient
			self.worldPosition[0] = new_pos[0]
			self.worldPosition[1] = new_pos[1]
		else:
			# Orien from normal hit
			hit_normal = self.targetObjectData[1]
			normal_vec = [-hit_normal[0], -hit_normal[1], hit_normal[2]]
			self.alignAxisToVect(normal_vec, 1, 1)

	def playStateTime(self, limit):
		""" Play state time with a limit
		"""
		if (self.stateTime < limit):
			self.stateTime += 0.1
			return False
		else:
			self.stateTime = limit
			return True

	def unsheat(self, active=True):
		self.fightManager.unsheat(active)

	def switchState(self, next_etat):
		# if the next state is the idle since applic reset same var
		if (next_etat == PlayerState.IDLE_STATE):
			self.ledgeCanceled = False
		# now applic the new state and reset stateTime
		self.stateTime = 0.0
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

	def respawnToGround(self):
		self.stopMovement()
		# stop orientation
		self.orientManager.stopOrientation(self)
		self.worldPosition = self.lastGroundPos
		self.worldPosition[2] = self.lastGroundPos[2] + + 1.2
		self.grounded = True
		self.fallTime = 0.0
		self.switchState(PlayerState.IDLE_STATE)

	def main(self, cont):
		# If player alive update
		if ( self.isAlive() ):
			# Pause menu
			if (self.gamepad.isPausePressed(logic.KX_INPUT_JUST_ACTIVATED)):
				logic.playerHUD.displayInventory()
				self.scene.suspend()

			# Process parry system
			self.targetManager.update()

			# update joystick/gamepad
			self.gamepad.updateJoystick()

			# Test if can always pick object
			self.pickManager.canAlwaysHold()

			# sword trail
			self.swordTrail.updateTrail()

			# Level manager
			if (self.tester.switchLevel()):
				return

			# If detect black hole
			if (self.tester.detectBlackHole() ):
				self.respawnToGround()
				return

			# track object
			if (self.targetManager.active):
				self.targetManager.updateTargetMode()
			else:
				# Find targetable object
				self.targetManager.findObject()
				# update axis orient
				self.orientManager.updateOrientController(self.worldPosition, scene.active_camera.worldOrientation.to_euler())
			#self.orient(cont)

			# If touch the ground, active ground physic else fall gravity
			if (self.grounded and self.onWater == False):
				self.physic.onGround()
			else :
				if (self.onLedge == False and self.onWater == False and self.onLadder == False):
					self.physic.gravity_fall()

			# Cam view and update
			self.camManager.cameraViewControl(self.gamepad)

			# Update mini map
			logic.playerHUD.updateMiniMap()

		# update state management
		managePlayerState(self)
		self.camManager.main()
		# update global dic data
		logic.player = self
		logic.globalDict['player'] = self
