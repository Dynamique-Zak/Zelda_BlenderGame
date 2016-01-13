from link_scripts.PlayerConstants import PlayerState

def firstLookViewState(self):
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
