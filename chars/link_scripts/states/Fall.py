from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Water import start_swimState
from link_scripts.StarterState import start_beginGrapLedgeState

def start_fallState(self):
	self.grounded = False
	self.fallTime = 0.0
	# go to idle state
	self.switchState(PlayerState.FALL_STATE)

def fallControl(self):
	LeftRight = 0
	UpDown = 0
	# control
	if ( self.gamepad.isLeftPressed() ):
		LeftRight = -0.2
	elif ( self.gamepad.isRightPressed() ):
		LeftRight = 0.2

	if ( self.gamepad.isDownPressed() ):
		UpDown = -0.1
	# apply
	self.linearMove(LeftRight, 0)
	self.linearMove(UpDown, 1)

def respawnToGround(self):
	self.stopMovement()
	# stop orientation
	self.orientManager.stopOrientation(self)
	self.worldPosition = self.lastGroundPos
	self.worldPosition[2] = self.lastGroundPos[2] + + 1.2
	self.grounded = True
	self.fallTime = 0.0
	self.switchState(PlayerState.IDLE_STATE)

def fallState(self):
	# If detect water
	if (self.tester.detectWater()):
		# reset
		self.fallTime = 0.0
		# stop orientation
		self.orientManager.stopOrientation(self)
		# start water
		start_swimState(self)
		# cancel method
		return

	# If detect black hole
	if (self.tester.detectBlackHole() ):
		respawnToGround(self)
		return

	# if touch the ground
	ground, point, normal = self.tester.groundRay()
	if (ground and self.fallTime > 0.3):
		print("touch the ground")
		# set grounded
		self.grounded = True
		# reset fall time
		self.fallTime = 0.0
		# go to land state
		self.switchState(PlayerState.LAND_STATE)
	else:
		# if detect the ledge and ledgeCanceled not true
		if (self.tester.detectLedge() and not self.ledgeCanceled):
			# do ledge
			self.fallTime = 0.0
			# go to ledge state
			#start_beginGrapLedgeState(self)
			self.switchState(PlayerState.START_GRAPLEDGE_STATE)
		else:
			# pla yfall anim
			self.rig.playFallDown()
			# fall control
			fallControl(self)
			# incrmeent tim
			self.fallTime += 0.1
