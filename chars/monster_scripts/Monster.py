from bge import logic, types
from random import randint
from monster_scripts.MonsterAudio import *
import aud
import os
import bpy

scene = logic.getCurrentScene()

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
sfxPath = bpy.path.abspath("//../audio/monster/")
# hit sounds
hitSound = aud.Factory(sfxPath + "enemy_hit.wav")

class Monster(types.KX_GameObject):

	def __init__(self, own, mesh, rig, attackBox):
		self.meshMonster = mesh
		self.rig = rig
		self.audio = MonsterAudio()
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
		self.attackLevel = 0
		self.etat = 0

	def stopMovement(self):
		self.linearVelocity[0] = 0.0
		self.linearVelocity[1] = 0.0

	def hitEffect(self):
		"""
		Hit effect
		"""
		effect = scene.addObject("strikeEffect1", self, 30)
		size = self.shufferedDamage * 2.0
		effect.scaling = [size, size, size]
		# change color to red
		self.meshMonster.color = [1, 0, 0, 1]
		# play hit sound
		device.play(hitSound)

	def endHitEffect(self):
		self.meshMonster.color = [1, 1, 1, 1]

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
