from link_scripts.PlayerConstants import PlayerState, FlipX
from link_scripts.states.Hits import start_hitState
from link_scripts.states.Attack import start_basicSwordAttack1State, start_jumpAttack, start_specialRollState

def start_leftStrafeRollState(self):
	self.targetManager.deactiveHeadTrack()
	self.rig.playStrafeRoll(FlipX.LEFT)
	# audio
	self.audio.playJumpSound()
	self.switchState(PlayerState.LEFT_STRAFE_ROLL_STATE)

def start_rightStrafeRollState(self):
	self.targetManager.deactiveHeadTrack()
	self.rig.playStrafeRoll()
	# audio
	self.audio.playJumpSound()
	self.switchState(PlayerState.RIGHT_STRAFE_ROLL_STATE)

def start_backJump(self):
	self.targetManager.deactiveHeadTrack()
	# Animation
	self.rig.playTargetFallBackJump()
	self.grounded = False
	self.stateTime = 0.0
	# Jump Movement
	self.linearVelocity[0] = 0.0
	self.linearVelocity[1] -= 7.0
	self.linearVelocity[2] += 10.5
	# audio
	self.audio.playJumpSound()
	# Change state
	self.switchState(PlayerState.FALL_BACK_JUMP_STATE)

def start_bounceBackJump(self):
	# Animation
	self.rig.playTargetBounceBackJump()
	self.stopMovement()
	self.grounded = True
	# Change state
	self.switchState(PlayerState.BOUNCE_BACK_JUMP_STATE)

def endTargetState(self):
	self.targetManager.deactivateTargetMode()

def hitFromTarget(self):
	# If detect enemy damage
	if (self.tester.detectEnemyDamage()):
		endTargetState(self)
		start_hitState(self)
		return True
	else :
		return False

#=================================================================
# * States
#=================================================================
def idleTargetState(self):
	# Process hit detect from target mode
	if (hitFromTarget(self)):
		return

	if (self.targetManager.active):
		if (self.targetManager.isHaveTargetObject()):
			self.targetManager.activeHeadTrack()
	else:
		endTargetState(self)
		self.switchState(PlayerState.IDLE_STATE)
		return
	# If respect ground rule
	if ( self.respectGroundRule(endTargetState) ):
		# if always found enemy and z key is holded
		if (self.targetManager.active and self.gamepad.isZPressed() ):
			# * Jump attack
			if (self.gamepad.isActionPressed() and self.fightManager.isUnsheated() ):
				if (self.targetManager.parry):
					start_specialRollState(self)
				else:
					start_jumpAttack(self)
				return

			# Basic combo attack
			if (self.gamepad.isAttackPressed() and self.fightManager.canUseSword()):
				if ( not self.fightManager.isUnsheated() ):
					self.unsheat()
				else:
					start_basicSwordAttack1State(self)

			elif ( self.targetManager.targetMovement(self) ):
				self.switchState(PlayerState.STRAFE_STATE)
			else:
				self.rig.playTargetIdle()
		else:
			self.switchState(PlayerState.IDLE_STATE)

def strafeState(self):
	# Process hit detect from target mode
	if (hitFromTarget(self)):
		return

	# If respect ground rule
	if ( self.respectGroundRule(endTargetState) ):
		if (self.targetManager.active and self.gamepad.isZPressed()):
			# if want straff roll
			if ( self.gamepad.isActionPressed() ):
				# if go to letf
				if ( self.gamepad.isRightPressed() ):
					start_rightStrafeRollState(self)
				# elif go to right
				elif (self.gamepad.isLeftPressed() ):
					start_leftStrafeRollState(self)
				# * Back jump (Salto)
				elif (self.gamepad.isDownPressed() ):
					start_backJump(self)
			# target movement
			elif ( self.targetManager.targetMovement(self) ):
				leftRight = True
				flip = FlipX.LEFT
				frames = []
				if (self.gamepad.isLeftPressed()):
					flip = FlipX.LEFT
					frames = [102, 103]
				elif (self.gamepad.isRightPressed()):
					flip = FlipX.RIGHT
					frames = [116, 117]
				# Play animation
				frame = self.rig.getActionFrame(5)
				if (leftRight):
					self.rig.playStrafeWard(flip)
					# Play sound
					self.audio.playStepSound(frame, frames)
				else:
					self.rig.playRun()
			else:
				self.switchState(PlayerState.IDLE_TARGET_STATE)
		else:
			self.switchState(PlayerState.IDLE_TARGET_STATE)

def leftStrafeRollState(self):
	# Process hit detect from target mode
	if (hitFromTarget(self)):
		return

	# if ANIMATION
	if ( not self.rig.isPlayingAction(5) ):
		# go idle strafe
		self.stopMovement()
		self.switchState(PlayerState.IDLE_TARGET_STATE)
	else:
		self.linearVelocity[0] = -9.0
		self.linearVelocity[1] = 2.5

def rightStrafeRollState(self):
	# Process hit detect from target mode
	if (hitFromTarget(self)):
		return

	# if ANIMATION
	if ( not self.rig.isPlayingAction(5) ):
		# go idle strafe
		self.stopMovement()
		self.switchState(PlayerState.IDLE_TARGET_STATE)
	else:
		self.linearVelocity[0] = 9.0
		self.linearVelocity[1] = 2.5

def fallBackJump(self):
	if (self.tester.detectGround() and self.playStateTime(0.6)):
		start_bounceBackJump(self)
	else:
		# Process hit detect from target mode
		hitFromTarget(self)

def bounceBackJump(self):
	if ( not self.rig.isPlayingAction(5)):
		self.rig.playBasePose()
		self.stopMovement()
		self.switchState(PlayerState.IDLE_TARGET_STATE)
	else:
		self.linearVelocity[1] = -2
