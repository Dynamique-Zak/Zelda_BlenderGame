from link_scripts.PlayerConstants import PlayerState

# ---------------------------------------------------------------------
# * PASTER
# ---------------------------------------------------------------------
def pasteToLedge(self):
	#set orientation to ledge
	hit_normal = self.ledgeData[1]
	normal_vec = [-hit_normal[0], -hit_normal[1], hit_normal[2]]
	self.alignAxisToVect(normal_vec, 1, 1)

	#set_pos
	z_pos = 0
	if ( self.physic.detectLedgeGround(3) ):
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

# ---------------------------------------------------------------------
# * STARTER
# ---------------------------------------------------------------------
def startGrapLedgeState(self):
	self.onLedge = True
	self.suspendDynamics()
	# block movement
	self.stopMovement()
	# go to wait ledge state
	self.switchState(PlayerState.GRAPLEDGE_STATE)

def start_beginGrapLedgeState(self):
	self.onLedge = True
	self.suspendDynamics()
	# block movement
	self.stopMovement()
	# paste
	#pasteToLedge(self)
	self.physic.pasteToLedge()
	# play anim
	self.rig.playStartGrapLedge()
	# go to begin grap ledge
	self.switchState(PlayerState.BEGIN_GRAPLEDGE_TO_GROUND_STATE)

# ---------------------------------------------------------------------
# * States
# ---------------------------------------------------------------------
def beginGrapLedgeToGround(self):
	if (self.rig.getActionFrame(3) == 20):
		# start to climb the ground
		start_climbLedgeState(self)
		# go t oclimb the ground state
		self.switchState(PlayerState.CLIMBLEDGE_STATE)

def grapLedgeState(self):
	"""
	Play grap ledge animation
	"""
	# if we want leave grap and fall (so is action key)
	if ( self.gamepad.isActionPressed() ):
		# deactivate ledge
		self.onLedge = False
		# restore the dynamcis who are suspend at last
		self.restoreDynamics()
		# set ledge canceled to true cause the player decide to leave ledge
		self.ledgeCanceled = True
		# go to fall state
		self.switchState(PlayerState.FALL_STATE)
		# cancel this method
		return

	# if have a ground near ledge
	if ( self.physic.detectLedgeGround() ):
		# detect if we want climb with up array key
		if ( self.gamepad.isUpPressed() ):
			start_climbLedgeState(self)
			# go to climb ledge state
			self.switchState(PlayerState.CLIMBLEDGE_STATE)
			# cancel this method
			return

	# block movement
	self.stopMovement()
	self.linearVelocity[2] = 0.0

	# play animation
	self.rig.playEdgeWait()

	#set orientation to ledge
	hit_normal = self.ledgeData[1]
	normal_vec = [-hit_normal[0], -hit_normal[1], hit_normal[2]]
	self.alignAxisToVect(normal_vec, 1, 1)

	#set_pos
	self.worldPosition[2] = self.ledgeData[2].worldPosition[2] - 0.0

def start_climbLedgeState(self):
	self.rig.playClimbLedge()

def climbLedgeState(self):
	"""
	Play climb ledge animation and applic new pos and state when the animation finished
	"""
	# if finish to climb
	if (self.rig.getActionFrame(3) == 95):
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
