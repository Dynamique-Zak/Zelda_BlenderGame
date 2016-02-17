#===================================================
# * Author : Schartier Isaac
# * Mail : schartier.isaac@gmail.com
# * Role : Project Manager
# * Created 12/02/16 at 20:09
#===================================================

# Import modules
import mathutils
from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Path import start_pathFollowState
from link_scripts.StarterState import start_pathFollowLevelState

# ---------------------------------------------------------------------
# * Starters
# ---------------------------------------------------------------------
def start_unlockDoorState(self):
	"""
	Documentation
	"""
	self.targetObject.parent['active'] = True
	self.switchState(PlayerState.UNLOCK_DOOR_STATE)

def start_afterOpenDoorState(self):
	"""
	Documentation
	"""
	self.switchState(PlayerState.AFTEROPEN_DOOR_STATE)

def start_openSlideDoorState(self):
	"""
	Documentation
	"""
	self.switchState(PlayerState.OPENSLIDE_DOOR_STATE)

def start_openDoorState(self):
	# Next state
	next_state = PlayerState.OPEN_DOOR_STATE
	# Active the target door animtion if not locked
	if ( not self.targetObject.parent['locked']):
		# set pos to door pos
		self.alignToTargetObject()
		# set open property
		self.targetObject['open'] = True
		self.targetObject['close'] = False
		# type = self.targetObject['door']
	else:
		# Test if can use dungeon key for unlock this door
		dungeon = self.targetObject.parent['dungeon']
		if ( not self.inventory.useDungeonKey(dungeon) ):
			# Return to idle state
			next_state = PlayerState.IDLE_STATE
	# switch state
	self.switchState(next_state)

# ---------------------------------------------------------------------
# * Utils
# ---------------------------------------------------------------------
def moveAfterDoor(self):
	self.rig.playRun()
	self.linearVelocity[0] = 0.0
	self.linearVelocity[1] = 8.0

# ---------------------------------------------------------------------
# * States
# ---------------------------------------------------------------------
def unlockDoorState(self):
	"""
	Documentation
	"""
	if ( not self.targetObject.parent['locked'] ):
		start_openDoorState(self)

def afterOpenDoorState(self):
	"""
	Documentation
	"""
	pathFollow = False

	if (self.tester.detectPath()):
		start_pathFollowState(self)
		pathFollow = True

	if ( self.playStateTime(3.0) or pathFollow ):
		# close the door
		self.targetObject['open'] = False
		self.targetObject['close'] = True
		# If not detected path follow
		if (not pathFollow):
			self.rig.playWait()
			self.stopMovement()
			self.camManager.setCameraAfterDoorClose()
			self.switchState(PlayerState.IDLE_STATE)
	else:
		# play run and move of player
		moveAfterDoor(self)

def openSlideDoorState(self):
	"""
	Documentation
	"""
	if ( self.playStateTime(5.0) ):
		start_afterOpenDoorState(self)

def openMechanicalDoor(self):
	frameDoor = self.targetObject.getActionFrame(0)
	if (frameDoor == 11):
		start_afterOpenDoorState(self)

def openRegularDoor(self):
	# if anim finish ed
	if (self.rig.getActionFrame(5) == 48):
		# if detect new
		if (self.tester.detectNextLevelSwitcher()):
		  start_pathFollowLevelState(self)
		else:
		  # go to idle
		  self.switchState(PlayerState.IDLE_STATE)

def openDoorState(self):
	if (self.targetObject.parent['locked']):
		start_unlockDoorState(self)
	else:
		start_openSlideDoorState(self)
	# type = self.targetObject['door']
	#
	# if type==0:
	# 	openMechanicalDoor(self)
	# else:
	# 	openRegularDoor(self)
