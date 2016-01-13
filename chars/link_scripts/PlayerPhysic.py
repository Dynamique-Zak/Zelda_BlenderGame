from bge import logic

scene = logic.getCurrentScene()
objects = scene.objects
# Get objects
forward_obj = objects['link_forward_obj']
ledge_ground_detect = objects['ledge_ground_detect']

class PlayerPhysic:

	def __init__(self, groundSens):
		self.groundSens = groundSens
		self.player = None

	def setPlayer(self, player):
		self.player = player

	def groundRay(self, add=0):
		posFrom = [self.player.worldPosition[0], self.player.worldPosition[1], self.player.worldPosition[2] - 0.1]
		posTo = [self.player.worldPosition[0], self.player.worldPosition[1], self.player.worldPosition[2] - 1.2 - add]
		prop = "ground"
		return self.player.rayCast(posTo, posFrom, 1.2, prop, 0, 1)

	def onGround(self):
		ground, pos, normal = self.groundRay(0)
		if (ground):
			self.player.linearVelocity[2] = 0.0
			self.player.worldPosition[2] = pos[2] + 1.0
			# if ground have field
			if ('field' in ground) :
				self.player.audio.setField(ground['field'])

	def detectGround(self):
		ground, pos, normal = self.groundRay(0)
		if (ground):
			return True
		else :
			return False

	def wallRay(self):
		"""
		Detect if touch the wall
		"""
		prop = "wall"
		return self.player.rayCast(forward_obj, self.player, 0.8, prop, 0, 1)

	def ledgeRay(self):
		"""
		Detect if touch a ledge
		"""
		prop = "ledge"
		return self.player.rayCast(forward_obj, None, 0.7, prop, 0, 1)

	def ledgeGroundRay(self, add=0):
		prop = "ground"
		return ledge_ground_detect.rayCast(forward_obj, None, 1.2+add, prop, 0, 1)

	def detectLedge(self):
		ledge, l_pos, l_normal = self.ledgeRay()
		# if touch ledge
		if (ledge):
			self.player.ledgeData[0] = l_pos
			self.player.ledgeData[1] = l_normal
			self.player.ledgeData[2] = ledge
			return True
		else:
			return False

	def detectLedgeGround(self, add=0):
		"""
		Detect if touch the ledge ground with ledgeGroubdRay and stock data in array
		"""
		ledge_ground, pos, normal = self.ledgeGroundRay(add)
		# if touch ledge
		if (ledge_ground):
			self.player.ledgeGroundData[0] = pos
			self.player.ledgeGroundData[1] = normal
			self.player.ledgeGroundData[2] = ledge_ground
			return True
		else:
			return False

	def gravity_fall(self):
		if (self.player.linearVelocity[2] > - 60):
			self.player.linearVelocity[2] -= 0.6

	def pasteToLedge(self):
		#set orientation to ledge
		hit_normal = self.player.ledgeData[1]
		normal_vec = [-hit_normal[0], -hit_normal[1], hit_normal[2]]
		self.player.alignAxisToVect(normal_vec, 1, 1)

		#set_pos
		z_pos = 0
		if ( self.detectLedgeGround(10) ):
			z_pos = self.player.ledgeGroundData[0][2] - 1
		else:
			z_pos = self.player.ledgeData[2].worldPosition[2]
		self.player.worldPosition[2] = z_pos
		self.player.linearVelocity[2] = 0.0
