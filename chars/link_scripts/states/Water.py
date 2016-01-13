from link_scripts.PlayerConstants import PlayerState
from link_scripts.StarterState import start_fallState
from link_scripts.states.Ledge import start_beginGrapLedgeState

def start_swimState(self):
	self.stopMovement()
	self.onWater = True
	self.grounded = False
	self.switchState(PlayerState.WAIT_SWIM_STATE)

def toWaterPos(self):
	self.worldPosition[2] = self.waterPos[2] - 0.3
	self.linearVelocity[2] = 0.0

def swimToGround(self):
	self.onWater = False
	self.grounded = True
	self.switchState(PlayerState.IDLE_STATE)

def forwardForce(self, forward_force):
	self.linearVelocity[0] = 0
	self.linearVelocity[1] = forward_force

def waitSwimState(self):
	# stop move
	self.stopMovement()
	# get forward force
	forward_force = self.getForwardForce()

	# past player to water
	toWaterPos(self)

	# if move go to forward swim state
	if (forward_force != 0):
		self.switchState(PlayerState.FORWARD_SWIM_STATE)
	else:
		# if detect ground ledge
		if ( self.physic.detectLedgeGround() and self.physic.detectLedge() ):
			if ( self.gamepad.isActionPressed() ):
				# deactivate water
				self.onWater = False
				# start climlb ledge
				start_beginGrapLedgeState(self)
				# cancel this method
				return
		# play animation
		self.rig.playSwimIdle()

def forwardSwimState(self):
	"""
	Forward swim state
	If detect ground specially g ot idle STATE
	"""
	# get forward force
	forward_force = self.getForwardForce() * 0.6

	# past player to water
	toWaterPos(self)

	# if detect the grounded
	if ( self.tester.detectGroundFromWater() ):
		# go to ground
		swimToGround(self)
		return

	# If always in water
	if (self.tester.detectWater()):
		# if move go to forward swim state
		if (forward_force != 0):
		   # forward movement
		   forwardForce(self, forward_force)
		   # play animation
		   self.rig.playSwimForward()
		   # active orientation movement
		   self.orientManager.orient_player(self)
		# else don"t move, go to wait swim state
		else:
			# stop orientation
			self.orientManager.stopOrientation(self)
			# go to wait swim
			self.switchState(PlayerState.WAIT_SWIM_STATE)
	# else out of water go to fall
	else:
		# stop orientation
		self.orientManager.stopOrientation(self)
		# stop movement
		self.stopMovement()
		# deactivate water
		self.onWater = False
		# go to fall
		start_fallState(self)
