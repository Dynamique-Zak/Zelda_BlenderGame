#===================================================
# * Author : Schartier Isaac
# * Mail : schartier.isaac@gmail.com
# * Role : Project Manager
# * Created 12/02/16 at 20:09
#===================================================

# Import modules
from link_scripts.PlayerConstants import PlayerState
from bge import logic
from link_scripts.StarterState import start_fallState
from link_scripts.states.Hits import start_hitState

scene = logic.getCurrentScene()
objects = scene.objects

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED

# ---------------------------------------------------------------------
# * Starters
# ---------------------------------------------------------------------
def start_spinSwordAttackState(self):
	"""
	Documentation
	"""
	self.rig.playSpinSwordAttack()
	self.switchState(PlayerState.SPINSWORD_ATTACK_STATE)

def start_waitSpinSwordAttackState(self):
	"""
	Documentation
	"""
	self.switchState(PlayerState.WAITSPINSWORD_ATTACK_STATE)

def start_basicSwordAttack1State(self):
	self.comboAttack += 1
	self.rig.playBasicSwordAttack1()
	self.switchState(PlayerState.BASIC_SWORD_ATTACK_1_STATE)

def start_basicSwordAttack2State(self):
	self.swordTrail.deactiveTrail()
	self.targetManager.deactiveHeadTrack()
	self.rig.playBasicSwordAttack2()
	self.switchState(PlayerState.BASIC_SWORD_ATTACK_2_STATE)

def start_basicSwordAttack3State(self):
	self.swordTrail.deactiveTrail()
	self.targetManager.deactiveHeadTrack()
	self.rig.playBasicSwordAttack3()
	self.switchState(PlayerState.BASIC_SWORD_ATTACK_3_STATE)

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
	self.switchState(PlayerState.BEGIN_JUMP_ATTACK_STATE)

def start_bounceJumpAttack(self):
	self.rig.playBounceJumpAttack()
	self.stopMovement()
	self.grounded = True
	self.switchState(PlayerState.BOUNCE_JUMP_ATTACK_STATE)

def start_clangSword(self):
	self.rig.playClangSword()
	self.stopMovement()
	self.switchState(PlayerState.CLANG_SWORD_STATE)

def start_specialRollState(self):
	self.targetManager.deactiveHeadTrack()
	self.stopMovement()
	# audio
	self.audio.playJumpSound()
	# Animation
	self.rig.playStrafeRoll()
	self.switchState(PlayerState.SPECIAL_ROLL_STATE)

def start_specialAttack(self):
	self.rig.playSpecialAttack1()
	self.grounded = False
	self.stopMovement()
	self.linearVelocity[2] += 15
	self.switchState(PlayerState.SPECIAL_ATTACK_1_STATE)

#======================================================
# * UTILS
#======================================================
def attackMove(self, speed):
	self.linearVelocity[0] = 0
	self.linearVelocity[1] = speed

def setDamage(damage):
	objects['sword_box_attack']['damage'] = damage

def detectClang(self):
	if (self.tester.swordTouchClang()):
		finishAttack(self, start_clangSword)
		return True
	else:
		return False

def finishAttack(self, function=None):
	self.cancelAttack()
	setDamage(0)
	if (function != None):
		function(self)
	else:
		if (self.targetManager.active):
			# go to idle target state
			self.switchState(PlayerState.IDLE_TARGET_STATE)
		else:
			# go to normal idle
			self.switchState(PlayerState.IDLE_STATE)

def detectDamageFromAttack(self):
	# If detect enemy damage
	if (self.tester.detectEnemyDamage()):
		self.cancelAttack()
		start_hitState(self)
		return True
	else:
		return False

# ---------------------------------------------------------------------
# * States
# ---------------------------------------------------------------------
def spinSwordAttackState(self):
	"""
	Documentation
	"""
	pass

def waitSpinSwordAttackState(self):
	"""
	Documentation
	"""
	pass

def basicSwordAttack1State(self):
	# If hitted by enemy
	if ( detectDamageFromAttack(self) ):
		return

	# IF fnish the sword attack
	frame = self.rig.getActionFrame(5)
	if ( frame == 13):
		finishAttack(self)
	else:
		# Clang Sword
		if (detectClang(self)):
			return
		self.audio.playAttack1Sound(frame, 4)
		self.audio.playSoundSwingFrame(frame, 5)
		# attack
		if (frame >= 3.0 and frame <= 5.0):
			self.swordTrail.activeTrail()
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
			if ( self.gamepad.isAttackPressed(JUST_ACTIVATED) ):
				if (self.comboAttack == 1):
					self.rig.stopAction(5)
					start_basicSwordAttack1State(self)
				else:
					start_basicSwordAttack2State(self)

def basicSwordAttack2State(self):
	# If hitted by enemy
	if ( detectDamageFromAttack(self) ):
		return

	# IF fnish the sword attack
	frame = self.rig.getActionFrame(5)
	if ( frame == 35):
		finishAttack(self)
	else:
		self.audio.playAttack1Sound(frame, 20, 1)
		self.audio.playSoundSwingFrame(frame, 21)
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
			if ( self.gamepad.isAttackPressed(JUST_ACTIVATED) ):
				start_basicSwordAttack3State(self)

def basicSwordAttack3State(self):
	# If hitted by enemy
	if ( detectDamageFromAttack(self) ):
		return

	# IF fnish the sword attack
	frame = self.rig.getActionFrame(5)
	if ( frame == 58):
		finishAttack(self)
	else:
		self.audio.playAttack1Sound(frame, 48, 2)
		self.audio.playSoundSwingFrame(frame, 49)
		# Attack power
		# Moving
		if( frame >= 42 and frame <= 52.0):
			setDamage(2)
			attackMove(self, 8)
		else:
			setDamage(0)
			attackMove(self, 0)

def fallJumpAttackState(self):
	# If hitted by enemy
	if ( detectDamageFromAttack(self) ):
		return

	if (self.tester.detectGround() and self.playStateTime(0.6)):
		start_bounceJumpAttack(self)
	else:
		self.tester.detectEnemyDamage()

def bounceJumpAttackState(self):
	# If hitted by enemy
	if ( detectDamageFromAttack(self) ):
		return

	frame = self.rig.getActionFrame(5)
	# If finish the attack
	if (frame == 89):
		finishAttack(self)
	# Clang Sword
	if (detectClang(self)):
		self.swordTrail.deactiveTrail()
		return
	# Sound
	self.audio.playAttack1Sound(frame, 79, 2)
	# Attack power
	if (frame >= 80 and frame <= 82):
		setDamage(3)
	else:
		setDamage(0)

def clangSwordState(self):
	frame = self.rig.getActionFrame(5)
	# If finish state
	if (frame == 110):
		# go to normal idle
		self.switchState(PlayerState.IDLE_STATE)
	else:
		if (frame < 103):
			self.linearVelocity[1] = -10.0
		else:
			self.stopMovement()

def specialRollState(self):
	frame = self.rig.getActionFrame(5)
	if ( not self.rig.isPlayingAction(5) ):
		start_specialAttack(self)
	else:
		self.linearVelocity[0] = 7
		if ( self.getDistanceTo(self.targetManager.targetObject) > 2.0 ):
			self.linearVelocity[1] = 10

def specialAttack1State(self):
	frame = self.rig.getActionFrame(5)
	if (frame >= 13):
		start_fallState(self)
	else:
		# Movement
		if ( frame <= 8 ):
			if ( self.getDistanceTo(self.targetManager.targetObject) > 2.0 ):
				self.linearVelocity[0] = 0
				self.linearVelocity[1] = 5
		else:
			self.stopMovement()
		# Sound
		self.audio.playAttack1Sound(frame, 1, 2)
		# Attack power
		if (frame >= 0 and frame <= 8):
			setDamage(5)
		else:
			setDamage(0)
