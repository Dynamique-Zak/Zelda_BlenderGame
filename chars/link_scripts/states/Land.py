from link_scripts.PlayerConstants import PlayerState

def lowLandState(self):
	# stop movement
	self.stopMovement()

	# play wait animation
	self.rig.playLowLand()

	# at the end of land animation
	if (self.rig.getActionFrame(1) >= 34):
		self.switchState(PlayerState.IDLE_STATE)
