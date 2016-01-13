from bge import logic

class PlayerLevelManager:
	
	def __init__(self):
		self.nextLevelName = ""
		self.step = 0
		self.pathObject = None
		self.transitionTime = 0.0
	
	def transitionIsFinish(self, end):
		if (self.transitionTime >= end):
			return True
		else:
			return False
		
	def changeLevel(self):
		logic.startGame("//../levels/" + self.nextLevelName + ".blend")