from bge import logic
from .StarterState import start_levelGapState, start_pathFollowState

scene = logic.getCurrentScene()
objects = scene.objects

# Get objects
forward_obj = objects['link_forward_obj']
detect_water_obj = objects['detect_water']

class PlayerTester:

	def __init__(self, player):
		self.player = player

	def detectWater(self):
		"""
		Detect if touch the ladder
		"""
		prop = "water"
		water, pos, normal = detect_water_obj.rayCast(self.player, None, 0.2, prop, 0, 1)
		if (water):
			self.player.waterPos = pos
			return True
		else:
			return False

	def detectLadder(self):
		"""
		Detect if touch the ladder
		"""
		prop = "ladder"
		ladder, pos, normal = self.player.rayCast(forward_obj, None, 0.8, prop, 0, 1)
		if (ladder):
			self.player.ladderData[0] = ladder
			self.player.ladderData[1] = normal
			return True
		else:
			return False

	def detectGroundFromWater(self):
		"""
		Detect if touch the ground from water
		"""
		prop = "ground"
		ground, pos, normal = self.player.rayCast(forward_obj, None, 2.0, prop, 0, 1)
		if (ground):
			return True
		else:
			return False

	def detectPath(self):
		"""
		Detect if touch the next level switcher
		"""
		prop = "path_follow"
		obj, pos, normal = self.player.rayCast(forward_obj, None, 0.8, prop, 0, 1)
		if (obj):
			# get property
			self.player.levelManager.pathObject = obj
			return True
		else :
			return False

	def detectDoor(self):
		"""
		Detect if touch a door
		"""
		prop = "door"
		door, pos, normal = self.player.rayCast(forward_obj, None, 0.8, prop, 0, 1)
		if (door):
			# get property
			self.player.targetObject = door
			return True
		else :
			return False

	def detectNextLevelSwitcher(self):
		"""
		Detect if touch the next level switcher
		"""
		prop = "changeLevel"
		obj, pos, normal = self.player.rayCast(forward_obj, None, 0.8, prop, 0, 1)
		if (obj):
			# get property
			self.player.levelManager.nextLevelName = obj['levelName']
			return True
		else :
			# test if find from the ground (
			posTo = [self.player.worldPosition[0], self.player.worldPosition[1], self.player.worldPosition[2] - 1.2]
			obj, pos, normal = self.player.rayCast(posTo, None, 1.2, prop, 0, 1)
			# detect
			if (obj and obj['type'] == 'gap'):
				# get property
				self.player.levelManager.nextLevelName = obj['levelName']
				self.player.levelManager.pathObject = obj
				return True
			else:
				return False

	def switchLevel(self):
		# if detect next-level
		if ( self.detectNextLevelSwitcher() ):
			# switch state to next level
			start_levelGapState(self.player)
			return True
		# else detect pall folow
		elif ( self.detectPath()):
			 start_pathFollowState(self.player)
			 return True
		else:
			 return False

	# =================================================================
	# * Pick Up Detection
	# =================================================================
	def detectObjectToPickUp(self):
		"""
		Detect if touch the ground from water
		"""
		prop = "pickable"
		testPos = [forward_obj.worldPosition[0], forward_obj.worldPosition[1], forward_obj.worldPosition[2] - 1.0]
		obj, pos, normal = self.player.rayCast(testPos, None, 2.0, prop, 0, 1)
		if (obj):
			self.player.objectPickable = obj
			return True
		else:
			return False

	# =================================================================
	# * Interactive detector
	# =================================================================
	def detectInteractivePlacard(self):
		"""
		Detect if touch the ground from water
		"""
		prop = "placard"
		placard, pos, normal = self.player.rayCast(forward_obj, None, 2.0, prop, 0, 1)
		if (placard):
			self.player.interaction.setMessage(placard['message'])
			return True
		else:
			return False
