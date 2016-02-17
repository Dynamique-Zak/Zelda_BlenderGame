from bge import logic, types
from random import randint
from monster_scripts.states.MushroomDekuStates import statesManager

# Constants
PLAY = logic.KX_ACTION_MODE_PLAY
LOOP = logic.KX_ACTION_MODE_LOOP

class MushroomDeku(types.KX_GameObject):

	def __init__(self, own, mesh, rig, attackBox):
		self.attackLevel = 0
		self.meshMonster = mesh
		self.rig = rig
		self.attackBox = attackBox
		self.targetObject = None
		self.targetMode = False
		self.energy = 6.0
		self.shufferedDamage = 0
		self.unusedVar = False
		self.stateTime = 0.0
		self.reactionTime = 0.0
		self.reactionDelay = 0.6
		self.startPos = self.worldPosition
		self.etat = 0

	def playSleep(self):
		""" Play idle animation
		"""
		self.rig.playAction(
		'mushroom_deku_idle', 61, 139,
		0, 2,
		0, LOOP)

	def playAppear(self):
		""" Play idle animation
		"""
		self.rig.playAction(
		'mushroom_deku_idle', 140, 169,
		0, 1,
		0, PLAY)

	def playIdle(self):
		""" Play idle animation
		"""
		self.rig.playAction(
		'mushroom_deku_idle', 1, 39,
		0, 1,
		5, LOOP)

	def playRun(self):
		""" Play run animation
		"""
		self.rig.playAction(
		'mushroom_deku_move', 1, 22,
		0, 1,
		2, LOOP)

	def playAttack(self):
		""" Play run animation
		"""
		self.rig.playAction(
		'mushroom_deku_move', 30, 66,
		0, 1,
		2, PLAY)

	def playHit(self):
		""" Play hit animation
		"""
		self.rig.playAction(
		'mushroom_deku_hit', 1, 21,
		0, 1,
		2, PLAY)

	def playLastHit(self):
		""" Play hit animation
		"""
		self.rig.playAction(
		'mushroom_deku_hit', 25, 70,
		0, 1,
		2, PLAY)

	def stopMovement(self):
		self.linearVelocity[0] = 0.0
		self.linearVelocity[1] = 0.0

	def switchState(self, state):
		self.etat = state

	def trackTo(self, obj):
		cont = logic.getCurrentController()
		act = cont.actuators['trackTo']
		if (obj != None):
			act.object = obj
			cont.activate('trackTo')
		else:
			cont.deactivate('trackTo')

	def isReactif(self, max):
		if (self.reactionTime + 0.1 >= max):
			print("lol")
			self.reactionTime = 0.0
			return True
		else:
			self.reactionTime += 0.1
			return False

	def playStateTime(self, max):
		if (self.stateTime + 1 < max):
			self.stateTime += 1
			return False
		else:
			self.stateTime = max
			return True

	def damage(self, value):
		if (self.energy - value < 0 ):
			self.energy = 0
		else:
			self.energy -= value

	def setAttack(self, power, type=0):
		self.attackBox['enemyDamage'] = power
		self.attackBox['type'] = type

	def generateRandomState(self, max):
		return randint(0, max)

	def isDead(self):
		if (self.energy == 0):
			return True
		else:
			return False

	def detectPlayer(self):
		cont = logic.getCurrentController()
		sens = cont.sensors['findPlayer']
		if sens.positive:
			self.targetObject = sens.hitObject
			return True
		else:
			return False

	def detectDamage(self, function):
		"""
		If detect damage call a function
		(general is a function for go to hit state)
		"""
		cont = logic.getCurrentController()
		sens = cont.sensors['touchDamage']
		if sens.positive and sens.hitObject['damage'] > 0.0:
			self.shufferedDamage = sens.hitObject['damage']
			self.trackTo(sens.hitObject)
			function(self)
			return True
		else:
			return False

	def main(self):
		statesManager(self)

def main(cont):
	own = cont.owner

	if not 'init' in own:
		mesh = None
		rig = None
		attackBox = None

		# Get rig and mesh obj
		for obj in own.children:
			if obj.name == "mushroomDeku_rig":
				rig = obj

		for obj in rig.children:
			if obj.name == "mushroomDeku_mesh":
				mesh = obj
			if obj.name == "mushroomDeku_attackBox":
				attackBox = obj

		# Make monster
		own = MushroomDeku(own, mesh, rig, attackBox)
		# Ok
		own['init'] = True
	else:
		own.main()
