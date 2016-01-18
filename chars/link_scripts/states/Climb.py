from link_scripts.PlayerConstants import PlayerState

def start_climbGroundState(self):
	pasteToWall(self)
	self.rig.playClimbLedge()
	self.switchState(PlayerState.CLIMBGROUND_STATE)


# ---------------------------------------------------------------------
# * PASTER
# ---------------------------------------------------------------------
def pasteToWall(self):
	#set orientation to ledge
	hit_normal = self.ledgeData[1]
	normal_vec = [-hit_normal[0], -hit_normal[1], hit_normal[2]]
	self.alignAxisToVect(normal_vec, 1, 1)

	#set_pos
	z_pos = self.ledgeGroundData[0][2] - 1.2

	self.worldPosition[2] = z_pos
	self.linearVelocity[2] = 0.0

def climbGroundState(self):
	"""
	Play climb ledge animation and applic new pos and state when the animation finished
	"""
	# if finish to climb
	if (self.rig.getActionFrame(3) == 95):
		self.rig.playBasePose()
		# paste player to ground (simule the climb pos
		ground_pos = self.ledgeGroundData[0]
		self.worldPosition[0] = ground_pos[0]
		self.worldPosition[1] = ground_pos[1]
		self.worldPosition[2] = ground_pos[2] + 1.2
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
