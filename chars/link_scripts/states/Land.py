from link_scripts.PlayerConstants import PlayerState

def lowLandState(self):
	# stop movement
	self.stopMovement()

	# at the end of land animation
	if (self.rig.getActionFrame(1) == 48):
		self.switchState(PlayerState.IDLE_STATE)
