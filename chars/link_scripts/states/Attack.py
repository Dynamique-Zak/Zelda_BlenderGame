from bge import logic
from link_scripts.PlayerConstants import *

scene = logic.getCurrentScene()
objects = scene.objects

def attackMove(self, speed):
	self.linearVelocity[0] = 0
	self.linearVelocity[1] = speed

def start_basicSwordAttack1State(self):
	self.comboAttack += 1
	self.rig.playBasicSwordAttack1()
	self.switchState(PlayerState.BASIC_SWORD_ATTACK_1)

def start_basicSwordAttack2State(self):
	self.targetManager.deactiveHeadTrack()
	self.rig.playBasicSwordAttack2()
	self.switchState(PlayerState.BASIC_SWORD_ATTACK_2)

def start_basicSwordAttack3State(self):
	self.targetManager.deactiveHeadTrack()
	self.rig.playBasicSwordAttack3()
	self.switchState(PlayerState.BASIC_SWORD_ATTACK_3)

def start_jumpAttack(self):
	# Animation
	self.rig.playBeginJumpAttack()
	self.stopMovement()
	self.grounded = False
	self.stateTime = 0.0
	self.linearVelocity[2] += 12.0
	self.linearVelocity[1] += 8.0
	self.linearVelocity[0] = 0.0
	# audio
	self.audio.playJumpSound()
	# Change state
	self.switchState(PlayerState.BEGIN_JUMP_ATTACK)

def start_bounceJumpAttack(self):
	self.rig.playBounceJumpAttack()
	self.stopMovement()
	self.grounded = True
	self.switchState(PlayerState.BOUNCE_JUMP_ATTACK)


def setDamage(damage):
	objects['sword_box_attack']['damage'] = damage

def finishAttack(self):
	# reset combo
	self.comboAttack = 0
	# reset damage
	setDamage(0)
	if (self.targetManager.active):
		# go to idle target state
		self.switchState(PlayerState.IDLE_TARGET_STATE)
	else:
		# go to normal idle
		self.switchState(PlayerState.IDLE_STATE)

def basicSwordAttack1State(self):
	# IF fnish the sword attack
	frame = self.rig.getActionFrame(5)
	if ( frame == 13):
		finishAttack(self)
	else:
		self.audio.playAttack1Sound(frame, 4)
		# attack
		if (frame >= 3.0 and frame <= 5.0):
			setDamage(1)
		else:
			setDamage(0)
		# Moving
		if( frame <= 3.0):
			attackMove(self, 5)
		else:
			attackMove(self, 0)
		# test combo
		if (frame >= 8.0):
			# next attack
			if ( self.gamepad.isAttackPressed() ):
				if (self.comboAttack == 1):
					self.rig.stopAction(5)
					start_basicSwordAttack1State(self)
				else:
					start_basicSwordAttack2State(self)

def basicSwordAttack2State(self):
	# IF fnish the sword attack
	frame = self.rig.getActionFrame(5)
	if ( frame == 35):
		finishAttack(self)
	else:
		self.audio.playAttack1Sound(frame, 20, 1)
		# attack
		if (frame >= 20 and frame <= 25):
			setDamage(1)
		else:
			setDamage(0)
		# Moving
		if( frame <= 25.0):
			attackMove(self, 5)
		else:
			attackMove(self, 0)
		if (frame >= 25.0):
			# next attack
			if ( self.gamepad.isAttackPressed() ):
				start_basicSwordAttack3State(self)

def basicSwordAttack3State(self):
	# IF fnish the sword attack
	frame = self.rig.getActionFrame(5)
	if ( frame == 58):
		finishAttack(self)
	else:
		self.audio.playAttack1Sound(frame, 48, 2)
		# Attack power
		# Moving
		if( frame >= 42 and frame <= 52.0):
			setDamage(2)
			attackMove(self, 8)
		else:
			setDamage(0)
			attackMove(self, 0)

def fallJumpAttackState(self):
	if (self.tester.detectGround() and self.playStateTime(0.6)):
		start_bounceJumpAttack(self)
	else:
		self.tester.detectEnemyDamage()

def bounceJumpAttackState(self):
	frame = self.rig.getActionFrame(5)
	# If finish the attack
	if (frame == 89):
		self.switchState(PlayerState.IDLE_STATE)
	# Sound
	self.audio.playAttack1Sound(frame, 79, 2)
	# Attack power
	if (frame >= 80 and frame <= 82):
		setDamage(3)
	else:
		setDamage(0)
