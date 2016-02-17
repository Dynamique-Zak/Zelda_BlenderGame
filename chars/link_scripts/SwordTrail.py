from bge import logic
from link_scripts.Trail import Trail

scene = logic.getCurrentScene()

def distP(a, b):
	return abs(a-b)

class SwordTrail:

	def __init__(self):
		sword = scene.objects['sword_trail']
		woosh = scene.objects['woosh']
		self.active = False
		self.trailEffect = Trail(True, 1, False, "x", False, sword, woosh)
		self.time = 0.0

	def nextFrame(self, max=0.4, speed=0.1):
		if (self.time + speed < max):
			self.time += speed
			return False
		else:
			self.time = 0.0
			return True

	def activeTrail(self):
		if (self.active == False):
			woosh = scene.objects['woosh']
			woosh.setVisible(True)
			self.active = True

	def deactiveTrail(self):
		if (self.active):
			woosh = scene.objects['woosh']
			woosh.setVisible(False)
			self.active = False

	def updateTrail(self):
		self.trailEffect.update()
