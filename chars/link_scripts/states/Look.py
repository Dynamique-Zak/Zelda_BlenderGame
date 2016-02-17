from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Hits import start_hitState

def start_firstLookView(self):
	self.orientManager.stopOrientation(self)
	self.stopMovement()
	self.camManager.camToFirstview()
	self.switchState(PlayerState.FIRST_LOOK_VIEW_STATE)

def endLook(self):
	# re activate tps camera mode
	self.camManager.activeTrackPlayer()

def firstLookViewState(self):
	# If detect enemy damage
	if (self.tester.detectEnemyDamage()):
		endLook(self)
		start_hitState(self)
		return

	# Look mode (Skills/object) Default bow
	if (self.objectManager.use):
		# Play target with object mode
		self.rig.playObjectTargetIdle()
		# * Object
		self.rig.playWaitBow()
	else:
		self.rig.playWait()

	# if cancel state
	if ( self.gamepad.isActionPressed() ):
		# re activate tps camera mode
		self.camManager.activeTrackPlayer()
		# go to idle state
		self.switchState(PlayerState.IDLE_STATE)
	# else use the first look view mode
	else:
		#init var
		LeftRight = 0.0
		UpDown = 0.0

		# Control part
		if ( self.gamepad.isLeftPressed() ):
			LeftRight = 0.05
		elif ( self.gamepad.isRightPressed() ):
			LeftRight = -0.05

		if ( self.gamepad.isUpPressed() ):
			UpDown = 0.05
		elif ( self.gamepad.isDownPressed() ):
			UpDown = -0.05

		# apply roation
		self.camManager.applyLook(UpDown, LeftRight)
