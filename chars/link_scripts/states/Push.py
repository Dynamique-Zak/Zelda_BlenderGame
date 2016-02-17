#===================================================
# * Author : Schartier Isaac
# * Mail : schartier.isaac@gmail.com
# * Role : Project Manager
# * Created 04/02/16 at 20:59
#===================================================

# Import modules
from link_scripts.PlayerConstants import PlayerState
from link_scripts.PlayerSound import PlayerSoundConstant
# ---------------------------------------------------------------------
# * Starters
# ---------------------------------------------------------------------
def start_walkPushState(self):
	"""
	Documentation
	"""
	self.audio.playAudio(PlayerSoundConstant.PUSH)
	self.audio.playAudio(PlayerSoundConstant.STEP_PUSH)
	self.rig.playWalkPush()
	self.switchState(PlayerState.WALK_PUSH_STATE)

def start_waitPushState(self):
	"""
	Documentation
	"""
	self.stopMovement()
	self.targetObject.worldLinearVelocity = [0, 0, 0]
	# Set orientation to bloc
	self.alignToTargetObject()
	# Play Animation
	self.rig.playWaitPush()
	self.switchState(PlayerState.WAIT_PUSH_STATE)

# ---------------------------------------------------------------------
# * End
# ---------------------------------------------------------------------
def end_pushState(self):
	self.stopMovement()
	self.switchState(PlayerState.IDLE_STATE)

# ---------------------------------------------------------------------
# * States
# ---------------------------------------------------------------------
def walkPushState(self):
	"""
	Documentation
	"""
	if ( not self.rig.isPlayingAction(4)):
		start_waitPushState(self)
	else:
		if ( self.tester.detectBloc() ):
			frame = self.rig.getActionFrame(4)
			# Push sound
			self.audio.playFrameSound(frame, [20], self.audio.getAudio(PlayerSoundConstant.STEP_PUSH))
			# Push Movement
			if ( frame < 34):
				self.linearVelocity[0] = 0.0
				self.linearVelocity[1] = 1.0
			else:
				self.stopMovement()
			self.targetObject.worldLinearVelocity[0] = self.worldLinearVelocity[0]
			self.targetObject.worldLinearVelocity[1] = self.worldLinearVelocity[1]
		else:
			end_pushState(self)

def waitPushState(self):
	"""
	Documentation
	"""
	if ( self.tester.detectBloc() ):
		# If can canel that state
		if (self.playStateTime(1.0)):
			# Can cancel now
			if ( self.gamepad.isActionPressed() ):
				# Cancel push state
				end_pushState(self)
				# Go to idle state
				self.switchState(PlayerState.IDLE_STATE)
				return
		# Presse forward for push the bloc
		if (self.gamepad.isUpPressed()):
			start_walkPushState(self)
	else:
		end_pushState(self)
