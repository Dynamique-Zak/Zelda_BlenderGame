import mathutils
from link_scripts.PlayerConstants import PlayerState
from link_scripts.StarterState import start_pathFollowLevelState

def applyNewPosition(self):
	self.worldPosition[1] += 1.0

def start_openDoorState(self):
	self.stateTime = 0.0
	# set pos to door pos
	door_pos = self.targetObject.worldPosition
	pos = mathutils.Vector([0, 0, 0])
	pos.rotate(self.targetObject.orientation)
	new_pos = pos + door_pos

	self.worldPosition[0] = new_pos[0]
	self.worldPosition[1] = new_pos[1]

	player_pos = self.worldPosition
	pos = mathutils.Vector([0, -1, 0])
	pos.rotate(self.orientation)
	self.worldPosition[0] += pos[0]
	self.worldPosition[1] += pos[1]
	# Now test the type of the door
	# active the target door animtion
	self.targetObject['open'] = True
	self.targetObject['close'] = False
	type = self.targetObject['door']

	if type == 1:
		# play anim
		self.rig.playOpenDoor()
		self.suspendDynamics()
		# switch state
	self.switchState(PlayerState.OPEN_DOOR_STATE)

def moveAfterDoor(self):
	self.rig.playRun()
	self.linearVelocity[0] = 0.0
	self.linearVelocity[1] = 8.0

def runAfterDoorState(self):
	if ( self.playStateTime(2.5) ):
		# close the door
		self.targetObject['open'] = False
		self.targetObject['close'] = True
		self.rig.playWait()
		self.stopMovement()
		self.camManager.setCameraAfterDoorClose()
		self.switchState(PlayerState.IDLE_STATE)
	else:
		# play run and move of player
		moveAfterDoor(self)

def openMechanicalDoor(self):
	frameDoor = self.targetObject.getActionFrame(0)
	if (frameDoor == 11):
		self.switchState(PlayerState.RUN_AFTER_DOOR_STATE)

def openRegularDoor(self):
	# if anim finish ed
	if (self.rig.getActionFrame(5) == 48):
		# change pos
		applyNewPosition(self)
		# if detect new
		if (self.tester.detectNextLevelSwitcher()):
		  start_pathFollowLevelState(self)
		else:
		  # go to idle
		  self.switchState(PlayerState.IDLE_STATE)

def openDoorState(self):
	type = self.targetObject['door']

	if type==0:
		openMechanicalDoor(self)
	else:
		openRegularDoor(self)
