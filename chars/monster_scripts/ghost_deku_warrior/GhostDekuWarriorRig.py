from bge import logic, types

# Constants
PLAY = logic.KX_ACTION_MODE_PLAY
LOOP = logic.KX_ACTION_MODE_LOOP

class GhostDekuWarriorRig(types.BL_ArmatureObject):
	def __init__(self, own):
		pass

	def playIdle(self):
		""" Play idle animation
		"""
		self.playAction(
		'gdw_move', 0, 26,
		0, 1,
		5, LOOP)

	def playWalk(self):
		""" Play run animation
		"""
		self.playAction(
		'gdw_move', 35, 95,
		0, 1,
		5, LOOP)

	def playPosture1(self):
		""" Play run animation
		"""
		self.playAction(
		'gdw_move', 100, 110,
		0, 1,
		1, PLAY)

	def playRun(self):
		""" Play run animation
		"""
		self.playAction(
		'gdw_move', 120, 133,
		0, 1,
		5, LOOP)

	def playAttack(self):
		""" Play run animation
		"""
		self.playAction(
		'gdw_attack', 0, 35,
		0, 1,
		2, PLAY)

	def playChargeAttack(self):
		""" Play run animation
		"""
		self.playAction(
		'gdw_attack', 40, 62,
		0, 1,
		2, PLAY)

	def playHit(self):
		""" Play hit animation
		"""
		self.stopAction(0)

		self.playAction(
		'gdw_hit', 1, 21,
		0, 1,
		2, PLAY)

	def playLastHit(self):
		""" Play hit animation
		"""
		self.playAction(
		'gdw_hit', 25, 70,
		0, 1,
		2, PLAY)
