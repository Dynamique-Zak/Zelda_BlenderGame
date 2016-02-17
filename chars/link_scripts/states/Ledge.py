#===================================================
# * Author : Schartier Isaac
# * Mail : schartier.isaac@gmail.com
# * Role : Project Manager
# * Created 12/02/16 at 20:09
#===================================================

# Import modules
from link_scripts.PlayerConstants import PlayerState
from link_scripts.PlayerSound import PlayerSoundConstant
# ---------------------------------------------------------------------
# * Utils
# ---------------------------------------------------------------------
def pasteToLedge(self):
	#set orientation to ledge
	hit_normal = self.ledgeData[1]
	normal_vec = [-hit_normal[0], -hit_normal[1], hit_normal[2]]
	self.alignAxisToVect(normal_vec, 1, 1)

	#set_pos
	z_pos = 0
	if ( self.tester.detectLedgeGround(3) ):
		z_pos = self.ledgeGroundData[0][2] - 1.2
	else:
		z_pos = self.player.ledgeData[2].worldPosition[2]
	self.worldPosition[2] = z_pos
	self.linearVelocity[2] = 0.0

def pasteToLedgeGround(self):
	# paste player to ground (simule the climb pos
	ground_pos = self.ledgeGroundData[0]
	self.worldPosition[0] = ground_pos[0]
	self.worldPosition[1] = ground_pos[1]
	self.worldPosition[2] = ground_pos[2] + 1.2
	# reset ground

def goToFallLedgeState(self):
	# deactivate ledge
	self.onLedge = False
	# restore the dynamcis who are suspend at last
	self.restoreDynamics()
	# set ledge canceled to true cause the player decide to leave ledge
	self.ledgeCanceled = True
	# go to fall state
	self.switchState(PlayerState.FALL_STATE)

# ---------------------------------------------------------------------
# * Starters
# ---------------------------------------------------------------------
def start_beginGrapLedgeState(self):
	# Play audio sound
	self.audio.playAudio(PlayerSoundConstant.GASP_LEDGE)
	# Active ledge
	self.onLedge = True
	# block movement
	self.stopMovement()
	self.suspendDynamics()
	#pasteToLedge(self)
	self.physic.pasteToLedge()
	# play anim
	self.rig.playStartGrapLedge()
	# go to begin grap ledge
	self.switchState(PlayerState.BEGINGRAP_LEDGE_STATE)

def start_grapLedgeState(self):
	self.switchState(PlayerState.GRAP_LEDGE_STATE)

def start_goToWaitLedgeState(self):
	# Play Animation
	self.rig.playGoToWaitLedge();
	self.switchState(PlayerState.GOTOWAIT_LEDGE_STATE)

def start_waitLedgeState(self):
	self.switchState(PlayerState.WAIT_LEDGE_STATE)

def startGrapLedgeState(self):
	self.onLedge = True
	self.suspendDynamics()
	# block movement
	self.stopMovement()
	# go to wait ledge state
	self.switchState(PlayerState.GRAPLEDGE_STATE)

def start_climbLedgeState(self):
	# Play audio sound
	self.audio.playAudio(PlayerSoundConstant.CLIMB_LEDGE)
	# Play Animation
	self.rig.playClimbLedge()
	self.switchState(PlayerState.CLIMB_LEDGE_STATE)

# ---------------------------------------------------------------------
# * States
# ---------------------------------------------------------------------
def beginGrapLedgeState(self):
	"""
	Documentation
	"""
	if ( not self.rig.isPlayingAction(3) ):
		start_grapLedgeState(self)

def grapLedgeState(self):
	"""
	Play grap ledge animation
	"""
	# block movement
	self.stopMovement()
	self.linearVelocity[2] = 0.0

	# play animation
	self.rig.playGrapLedge();

	#set orientation to ledge
	hit_normal = self.ledgeData[1]
	normal_vec = [-hit_normal[0], -hit_normal[1], hit_normal[2]]
	self.alignAxisToVect(normal_vec, 1, 1)

	#set_pos
	self.worldPosition[2] = self.ledgeData[2].worldPosition[2] - 0.0

	# If we want leave grap and fall (so is action key)
	if ( self.gamepad.isActionPressed() ):
		# cancel this method
		goToFallLedgeState(self)

	# Else if have a ground near ledge and state time == 0.6
	elif ( self.tester.detectLedgeGround() and self.playStateTime(0.6) ):
		# Detect if we want climb with up array key
		if ( self.gamepad.isUpPressed() ):
			# Go to wait ledge
			start_goToWaitLedgeState(self)

def goToWaitLedgeState(self):
	"""
	Documentation
	"""
	if ( not self.rig.isPlayingAction(3) ):
		start_waitLedgeState(self)

def waitLedgeState(self):
	"""
	Documentation
	"""
	# Wait edge anim
	self.rig.playEdgeWait()

	# If we want leave grap and fall (so is action key)
	if ( self.gamepad.isActionPressed() ):
		# cancel this method
		goToFallLedgeState(self)

	# if have a ground near ledge and state time == 0.6
	elif ( self.tester.detectLedgeGround() and self.playStateTime(0.6) ):
		# detect if we want climb with up array key
		if ( self.gamepad.isUpPressed() ):
			start_climbLedgeState(self)

def climbLedgeState(self):
	"""
	Play climb ledge animation and applic new pos and state when the animation finished
	"""
	# if finish to climb
	if ( not self.rig.isPlayingAction(3) ):
		self.rig.playBasePose()
		# paste player to ground (simule the climb pos
		pasteToLedgeGround(self)
		# set ledge to false
		self.onLedge = False
		self.grounded = True
		self.restoreDynamics()
		# go to idle state
		self.switchState(PlayerState.IDLE_STATE)
	else:
		# paste player to ledge always (imagin ledge can move
		# block movement
		self.stopMovement()
		self.linearVelocity[2] = 0.0
