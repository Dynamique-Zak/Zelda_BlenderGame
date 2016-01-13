from link_scripts.PlayerConstants import PlayerState

def jumpState(self):
	# set ground to false
	self.grounded = False
	# jump force
	self.linearVelocity[2] += 13.0
	#test if y_force is respectable
	if (self.linearVelocity[1] > 12.0):
		self.linearVelocity[1] = 12.0
	# play jump
	self.rig.playJump()
	# change state to fall
	self.switchState(PlayerState.FALL_STATE)
