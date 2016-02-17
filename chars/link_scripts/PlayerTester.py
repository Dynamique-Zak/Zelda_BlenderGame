from bge import logic
from link_scripts.states.Path import start_pathFollowState
from .states.SwitchLevel import start_switchLevel

scene = logic.getCurrentScene()
objects = scene.objects

# Get objects
forward_obj = objects['link_forward_obj']
detect_water_obj = objects['detect_water']
ledge_ground_detect = objects['ledge_ground_detect']

class PlayerTester:

	def __init__(self, player):
		self.player = player

	def groundRay(self, add=0):
		posTo = [self.player.worldPosition[0], self.player.worldPosition[1], self.player.worldPosition[2] - 1.2]
		prop = "ground"
		return self.player.rayCast(posTo, None, 1.2+add, prop, 0, 1)

	def detectGround(self):
		"""
		If detect the ground with groundRay save the last ground pos
		for respawn and return True
		"""
		ground, pos, normal = self.groundRay(0)
		if (ground):
			self.player.lastGroundPos = pos
			return True
		else :
			return False

	def detectBlackHole(self):
		"""
		If detect a blackHole/gulf, return True
		"""
		posTo = [self.player.worldPosition[0], self.player.worldPosition[1], self.player.worldPosition[2] - 1.2]
		prop = "blackHole"
		obj, pos, normal = self.player.rayCast(posTo, None, 1.2, prop, 0, 1)
		if (obj):
			return True
		else:
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
		"""
		Detect a ground on top of a ledge
		"""
		prop = "ground"
		return ledge_ground_detect.rayCast(forward_obj, None, 0.6+add, prop, 0, 1)

	def detectLedge(self):
		"""
		Detect ledge, if can detect the ledge, save ledge data into array
		for process ledge system
		"""
		ledge, l_pos, l_normal = self.ledgeRay()
		# if touch ledge
		if (ledge):
			self.player.ledgeData[0] = l_pos
			self.player.ledgeData[1] = l_normal
			self.player.ledgeData[2] = ledge
			return True
		else:
			return False

	def detectLedgeBottom(self):
		"""
		If detect the ledge from bottom of player
		"""
		# To Do

	def detectLedgeGround(self, add=0):
		"""
		Detect if touch the ledge ground with ledgeGroundRay and stock data in array
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

	def detectWater(self):
		"""
		Detect if touch the water
		Else he fall fast ,detect from up also
		"""
		isCheck = False
		prop = "water"
		water, pos, normal = detect_water_obj.rayCast(self.player, None, 0.2, prop, 0, 1)
		if (water):
			self.player.waterPos = pos
			isCheck = True
		else:
			# Else if can see the from up
			dw_pos = detect_water_obj.worldPosition
			pos = [dw_pos[0], dw_pos[1], dw_pos[2] + 1.0]
			water, pos, normal = detect_water_obj.rayCast(pos, None, 0.5, prop, 0, 1)
			if (water):
				self.player.waterPos = pos
				isCheck = True
		# return finally statement
		return isCheck

	def detectLadder(self):
		"""
		Detect if touch the ladder, if detect save ladder data for
		process the climbLadderSystem
		Note: Detect ladder from forward
		"""
		prop = "ladder"
		ladder, pos, normal = self.player.rayCast(forward_obj, None, 0.8, prop, 0, 1)
		if (ladder):
			self.player.ladderData[0] = ladder
			self.player.ladderData[1] = normal
			self.player.audio.setField(ladder['field'])
			return True
		else:
			return False

	def detectLadderBottom(self):
		"""
		If detect a ladder from bottom of player
		"""
		posTo = [self.player.worldPosition[0], self.player.worldPosition[1], self.player.worldPosition[2] - 1.2]
		prop = "ladder_top"
		ladder, pos, normal = self.player.rayCast(posTo, None, 1.3, prop, 0, 1)
		if (ladder):
			self.player.ladderData[0] = ladder
			self.player.ladderData[1] = normal
			self.player.audio.setField(ladder.parent['field'])
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

	def detectLedgeGroundFromGround(self):
		"""
		Detect if touch the ground with ledgefrom the ground
		"""
		if (self.detectLedge() and self.detectLedgeGround()):
			return True
		else :
			return False

	def detectPath(self):
		"""
		Detect if touch a path follow, can use from switch level
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
		door, pos, normal = self.player.rayCast(forward_obj, None, 1.5, prop, 0, 1)
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
			logic.globalDict['level']['startPos'] = eval(obj['startPos'])
			logic.globalDict['level']['targetVec'] = eval(obj['targetVec'])
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
			start_switchLevel(self.player)
			return True
		else:
			 return False

	# =================================================================
	# * Hit detector
	# =================================================================
	def detectEnemyDamage(self):
		"""
		Detect enemy attack, when touch property enemyDamage so the player was hit
		Save shuffered damage for futur process(Hit effect, etc)
		"""
		cont = logic.getCurrentController()
		sens = cont.sensors['detectDamage']
		if ( sens.positive and sens.hitObject['enemyDamage'] ):
			self.player.shufferedDamage = sens.hitObject['enemyDamage']
			return True
		else:
			return False

	def swordTouchClang(self):
		cont = logic.getCurrentController()
		sens = cont.sensors['sword_touch_clang']
		if ( sens.positive ):
			return True
		else:
			return False
	# =================================================================
	# * Pick Up Detection
	# =================================================================
	def detectObjectToPickUp(self):
		"""
		Detect if can pick a object
		"""
		cont = logic.getCurrentController()
		sens = cont.sensors['detectPickable']
		if sens.positive:
			self.player.pickManager.pickedObject = sens.hitObject
			return True
		else:
			return False

	# =================================================================
	# * Interactive detector
	# =================================================================
	def detectInteractivePlacard(self):
		"""
		Detect if can read a placard
		"""
		prop = "placard"
		placard, pos, normal = self.player.rayCast(forward_obj, None, 2.0, prop, 0, 1)
		if (placard):
			self.player.interaction.setMessage(placard['message'])
			return True
		else:
			return False

	# =================================================================
	# * Object Interactiion
	# =================================================================
	def detectBloc(self):
		"""
		Detect bloc object
		"""
		prop = "bloc"
		bloc, pos, normal = self.player.rayCast(forward_obj, None, 1.0, prop, 0, 1)
		if (bloc and bloc["bloc"]):
			self.player.targetObject = bloc
			self.player.targetObjectData = [pos, normal]
			return True
		else:
			return False

	def detectChest(self):
		"""
		Detect chest object
		"""
		prop = "chest"
		chest, pos, normal = self.player.rayCast(forward_obj, None, 1.0, prop, 0, 1)
		if (chest and chest["open"] == False and chest["alreadyOpen"] == False ):
			self.player.targetObject = chest
			self.player.targetObjectData = [pos, normal]
			return True
		else:
			return False
