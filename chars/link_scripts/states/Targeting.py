from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Attack import start_basicSwordAttack1State

def start_leftStrafeRollState(self):
	self.rig.playRightStrafeRoll()
	self.switchState(PlayerState.LEFT_STRAFE_ROLL_STATE)

def start_rightStrafeRollState(self):
	self.rig.playRightStrafeRoll()
	self.switchState(PlayerState.RIGHT_STRAFE_ROLL_STATE)

def endTargetState(self):
	self.targetManager.deactivateTargetMode()

def idleTargetState(self):
	# If respect ground rule
	if ( self.respectGroundRule(endTargetState) ):
		# if z key is holded
		if ( self.gamepad.isZPressed() ):
			if (self.gamepad.isAttackPressed()):
				if (self.armed == False):
					self.activeArmedMode()
				else:
					start_basicSwordAttack1State(self)
			elif ( self.targetManager.targetMovement(self) ):
				self.switchState(PlayerState.STRAFE_STATE)
			else:
				self.rig.playTargetIdle()
		else:
			self.targetManager.deactivateTargetMode()
			self.switchState(PlayerState.IDLE_STATE)

def strafeState(self):
	# If respect ground rule
	if ( self.respectGroundRule(endTargetState) ):
		# if want straff roll
		if ( self.gamepad.isActionPressed() ):
			# if go to letf
			if ( self.gamepad.isRightPressed() ):
				start_rightStrafeRollState(self)
			# elif go to right
			elif (self.gamepad.isLeftPressed() ):
				start_leftStrafeRollState(self)
		# target movement
		elif ( self.targetManager.targetMovement(self) ):
			# play ANIMATION
			self.rig.playStrafeWard()
		else:
			self.switchState(PlayerState.IDLE_TARGET_STATE)

def leftStrafeRollState(self):
	# if ANIMATION
	if ( self.rig.getActionFrame(5) == 40):
		# go idle strafe
		self.stopMovement()
		self.switchState(PlayerState.IDLE_TARGET_STATE)
	else:
		self.linearVelocity[0] = -6.0
		self.linearVelocity[1] = 2.5

def rightStrafeRollState(self):
	# if ANIMATION
	if ( self.rig.getActionFrame(5) == 40):
		# go idle strafe
		self.stopMovement()
		self.switchState(PlayerState.IDLE_TARGET_STATE)
	else:
		self.linearVelocity[0] = 6.0
		self.linearVelocity[1] = 2.5
