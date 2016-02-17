from bge import logic

class HeartContainer:

	def __init__(self, startHeart, maxHeart):
		self.isLow = False
		# if heartContainer not exist init then
		if not 'heartContainer' in logic.globalDict['Player']:
			logic.globalDict['Player']['heartContainer'] = {'heart' : startHeart, 'maxHeart' : maxHeart}

	def calculLow(self):
		heartContainer = logic.globalDict['Player']['heartContainer']
		percent = (heartContainer['heart']/heartContainer['maxHeart']) * 100
		if (percent < 40):
			self.isLow = True
		else:
			self.isLow = False
		logic.playerHUD.low_healt(self.isLow)

	def load(self, startHeart, maxHeart):
		heartContainer = logic.globalDict['Player']['heartContainer']
		heartContainer['heart'] = startHeart
		heartContainer['maxHeart'] = maxHeart

	def gainHeart(self, qte):
		"""
		Gain heart, if the gain exceeds then set to max heart
		"""
		heartContainer = logic.globalDict['Player']['heartContainer']
		next_heart = heartContainer['heart'] + qte
		if (next_heart > heartContainer['maxHeart']):
			heartContainer['heart'] = heartContainer['maxHeart']
		else:
			heartContainer['heart'] = next_heart
		# Update hud and lowHeart state
		self.calculLow()
		logic.playerHUD.updateHeart()

	def loseHeart(self, qte):
		"""
		Lost heart, if the lose exceeds then set to zero
		"""
		heartContainer = logic.globalDict['Player']['heartContainer']
		next_heart = heartContainer['heart'] - qte
		if (next_heart < 0):
			heartContainer['heart'] = 0
		else:
			# calculLow
			self.calculLow()
			heartContainer['heart'] = next_heart
		# Update hud and lowHeart state
		logic.playerHUD.updateHeart()

	def notHaveHeart(self):
		heartContainer = logic.globalDict['Player']['heartContainer']
		if ( heartContainer['heart'] == 0 ) :
			return True
		else:
			return False

class RupeeContainer:

	def __init__(self, startRupee, maxRupee):
		# if heartContainer not exist init then
		if not 'rupeeContainer' in logic.globalDict['Player']:
			logic.globalDict['Player']['rupeeContainer'] = {'rupee' : startRupee, 'maxRupee' : maxRupee}

	def gainRupee(self, qte):
		"""
		Gain heart, if the gain exceeds then set to max heart
		"""
		rupeeContainer = logic.globalDict['Player']['rupeeContainer']
		next_rupee = rupeeContainer['rupee'] + qte
		if (next_rupee > rupeeContainer['maxRupee']):
			rupeeContainer['rupee'] = rupeeContainer['maxRupee']
		else:
			rupeeContainer['rupee'] = next_rupee
		# Update hud
		logic.playerHUD.updateRupee()
