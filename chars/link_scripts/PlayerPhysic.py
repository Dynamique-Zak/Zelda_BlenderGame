from bge import logic

scene = logic.getCurrentScene()
objects = scene.objects
# Get objects
forward_obj = objects['link_forward_obj']

class PlayerPhysic:

	def __init__(self):
		self.player = None

	def setPlayer(self, player):
		self.player = player

	def onGround(self):
		ground, pos, normal = self.player.tester.groundRay(0)
		if (ground):
			self.player.linearVelocity[2] = 0.0
			self.player.worldPosition[2] = pos[2] + 1.0
			# if ground have field
			if ('field' in ground) :
				self.player.audio.setField(ground['field'])

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
		if ( self.player.tester.detectLedgeGround(10) ):
			z_pos = self.player.ledgeGroundData[0][2] - 1
		else:
			z_pos = self.player.ledgeData[2].worldPosition[2]
		self.player.worldPosition[2] = z_pos
		self.player.linearVelocity[2] = 0.0
