from bge import logic
import aud
import os
import bpy

scene = logic.getCurrentScene()

# load sound device
device = aud.device()
# load sound file (it can be a video file with audio)
sfxPath = bpy.path.abspath("//../audio/monster/gwd/")
#
laughtSound = aud.Factory(sfxPath + "knuckle_attack.wav")
laughtRunSound = aud.Factory(sfxPath + "knuckle_run.wav")
hitLaughtSound = aud.Factory(sfxPath + "knuckle_hurt.wav")
step = aud.Factory(sfxPath + "../enemy_bounce.wav")

swordSound = aud.Factory(sfxPath + "../../obj_sfx/sword_swing.wav")
# bounceSound = aud.Factory(sfxPath + "enemy_bounce.wav")

# States
SLEEP_STATE = 0
IDLE_STATE = 1
WALK_STATE = 2
RUN_STATE = 3
POSTURE_STATE = 4
CHARGE_ATTACK_STATE = 5
ATTACK_STATE = 6
HIT_STATE = 7
LAST_HIT_STATE = 8
APPEAR_STATE = 9
DEAD_STATE = 10

# ====================================================
# * Starter and UTILS
# ====================================================
def start_attackState(self):
	# Deactivate the track
	self.trackTo(None)
	# Attack level to 1
	self.attackLevel = 1
	# Play laught sound
	device.play(laughtSound)
	# Start anim
	self.rig.playAttack()
	# Go t oattack state
	self.switchState(ATTACK_STATE)

def start_hitState(self):
	device.play(hitLaughtSound)
	end_attackState(self)
	# Play animation
	self.rig.playHit()
	self.stopMovement()
	self.hitEffect()
	self.switchState(HIT_STATE)

def start_postureState(self):
	# Play animation
	self.rig.playPosture1()
	# Audio
	device.play(laughtRunSound)
	self.stopMovement()
	self.switchState(POSTURE_STATE)

def start_chargeAttack(self):
	# Deactivate the track
	self.trackTo(None)
	# Player can party
	self.attackLevel = 2
	# Play animation
	self.rig.playChargeAttack()
	# Play laught sound
	device.play(laughtSound)
	# Go to charge attack state
	self.switchState(CHARGE_ATTACK_STATE)

def end_attackState(self):
	self.attackLevel = 0
	self.setAttack(0)

def appearState(self):
	pass


# ====================================================
# * States
# ====================================================
def idleState(self):
	"""
	Idle/Wait state
	"""
	self.stopMovement()
	# Play animation
	self.rig.playIdle()

	# Detect damage
	if self.detectDamage(start_hitState):
		return

	# If detect play go to it
	if ( self.detectPlayer()):
		self.trackTo(self.targetObject)
		distance = self.getDistanceTo(self.targetObject)
		if (distance > 3.0):
			self.switchState(WALK_STATE)
		# Near player
		else:
			# Reaction delay
			if (self.isReactif(5.6)):
				start_attackState(self)

def walkToPlayerState(self):
	"""
	Walk state - Approching the player between a distance
	"""
	# Play animation
	self.rig.playWalk()
	# get var
	frame = self.rig.getActionFrame(0)
	goToIdle = False
	# If detect play go to it
	if ( self.detectPlayer()):
		distance = self.getDistanceTo(self.targetObject)

		# Play step sound
		self.audio.playStepSound(frame, [48, 79], step)
		if (distance > 3.0 and distance < 8):
			if ( not (frame >= 78 and frame <= 91) and not (frame >= 47 and frame <= 60) ):
				self.linearVelocity[1] = 2.0
			else:
				self.stopMovement()
		elif (distance >= 8):
			start_postureState(self)
		else:
			goToIdle = True
	else:
		goToIdle = True
	# Else near player
	if (goToIdle):
		self.stopMovement()
		self.switchState(IDLE_STATE)

def runState(self):
	"""
	Run state (after posture state)
	"""
	# If detect play go to it
	if ( self.detectPlayer()):
		distance = self.getDistanceTo(self.targetObject)

		if (distance > 5.0):
			# Play animation
			self.rig.playRun()

			frame = self.rig.getActionFrame(0)
			# Play step sound
			self.audio.playStepSound(frame, [123, 130], step)

			# Movement
			self.linearVelocity[0] = 0.0
			self.linearVelocity[1] = 8.0
		else:
			# Start charge attack stat
			start_chargeAttack(self)

def postureState(self):
	"""
	Posture state (before running to player)
	"""
	# If animation finish
	if ( not self.rig.isPlayingAction(0) ):
		self.switchState(RUN_STATE)

def chargeAttackState(self):
	"""
	Charge attack state (after running)
	"""
	# If animation finish
	if ( not self.rig.isPlayingAction(0) ):
		self.switchState(IDLE_STATE)
	else:
		frame = self.rig.getActionFrame(0)

		# Set Attack Power
		if (frame >= 50 and frame < 55):
			self.setAttack(1)
		else:
			# Attack 0
			self.setAttack(0)

		# Audio
		if (frame >= 52 and frame <= 53):
			device.play(swordSound)

		# If can't parry
		if (frame > 44.0):
			self.attackLevel = 0

		# Stop movement at 54
		if (frame >= 54):
			self.stopMovement()

def attackState(self):
	"""
	Basic attack state (when player is near)
	"""
	# Deactivate track
	self.trackTo(None)

	# Finish
	if ( not self.rig.isPlayingAction(0) ):
		end_attackState(self)
		self.switchState(IDLE_STATE)
	else:
		frame = self.rig.getActionFrame(0)
		# Set Attack Power
		if (frame >= 12 and frame < 18):
			self.setAttack(1)
		else:
			# Attack 0
			self.setAttack(0)
			# Detect damage
			if self.detectDamage(start_hitState):
				return

		# If can't parry
		if (frame > 8.0):
			self.attackLevel = 0
		# Audio
		if (frame >= 13 and frame <=14):
			device.play(swordSound)

def hitState(self):
	"""
	Basic Hit state
	"""
	if ( not self.rig.isPlayingAction(0)):
		self.switchState(IDLE_STATE)
	else:
		frame = self.rig.getActionFrame(0)
		if (frame >= 5):
			self.endHitEffect()
		if (frame > 6):
			# Detect damage
			if self.detectDamage(start_hitState):
				return

def lastHitState(self):
	pass

def deadState(self):
	# Dead
	self.endObject()

def statesManager(self):
	etat = self.etat
	if (etat == APPEAR_STATE):
		appearState(self)

	elif (etat == IDLE_STATE):
		idleState(self)

	elif (etat == WALK_STATE):
		walkToPlayerState(self)

	elif (etat == RUN_STATE):
		runState(self)

	elif (etat == POSTURE_STATE):
		postureState(self)

	elif (etat == CHARGE_ATTACK_STATE):
		chargeAttackState(self)

	elif (etat == ATTACK_STATE):
		attackState(self)

	elif (etat == HIT_STATE):
		hitState(self)

	elif (etat == LAST_HIT_STATE):
		lastHitState(self)

	elif (etat == DEAD_STATE):
		deadState(self)
