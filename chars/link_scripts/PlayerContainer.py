from bge import logic

class HeartContainer:

	def __init__(self, startHeart, maxHeart):
		# if heartContainer not exist init then
		if not 'heartContainer' in logic.globalDict['Player']:
			logic.globalDict['Player']['heartContainer'] = {'heart' : startHeart, 'maxHeart' : maxHeart}

	def gainHeart(self, qte):
		"""
		Gain heart, if the gain exceeds then set to max heart
		"""
		heartContainer = logic.globalDict['Player']['heartContainer']
		next_heart = heartContainer['heart'] + qte
		if (next_heart > self.maxHeart):
			heartContainer['heart'] = logic.globalDict['maxHeart']
		else:
			heartContainer['heart'] = next_heart

	def loseHeart(self, qte):
		"""
		Lost heart, if the lose exceeds then set to zero
		"""
		heartContainer = logic.globalDict['Player']['heartContainer']
		next_heart = heartContainer['heart'] - qte
		if (next_heart < 0):
			heartContainer['heart'] = 0
		else:
			heartContainer['heart'] = next_heart

class RupeeContainer:

	def __init__(self, startRupee, maxRupee):
		# if heartContainer not exist init then
		if not 'rupeeContainer' in logic.globalDict['Player']:
			logic.globalDict['Player']['rupeeContainer'] = {'rupee' : startRupee, 'maxRupee' : maxRupee}
