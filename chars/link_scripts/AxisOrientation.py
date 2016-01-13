from bge import logic, types

class AxisOrientation(types.KX_GameObject):
	
	def __init__(self, own):
		pass
		
	def update(self, pos, orient):
		self.worldPosition = pos
		self.worldOrientation = orient