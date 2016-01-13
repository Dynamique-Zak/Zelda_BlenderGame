from bge import logic
from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Water import start_swimState

def start_rollState(self):
	# reset hud action text
	#logic.globalDict['PlayerHUD'].resetActionText()
	# force movement
	self.linearVelocity[1] += 3.0
	self.rig.playRoll()

def start_rollWall(self):
	# stop movement
	self.stopMovement()
	self.linearVelocity[1] -= 6.0
	# play animation
	self.rig.playRollWall()

def stop_rollWall_force(self):
	if (self.linearVelocity[1] < 0.0):
		self.linearVelocity[1] += 0.2
	else:
		self.linearVelocity[1] = 0.0

def rollState(self):
	# If detect water
	if (self.tester.detectWater()):
		# stop orientation
		self.orientManager.stopOrientation(self)
		# go to swim
		start_swimState(self)
	else:
		# if detect always the ground continue the rolling
		if (self.physic.detectGround()):
			wall, pos, normal = self.physic.wallRay()
			if (wall):
				start_rollWall(self)
				self.switchState(PlayerState.ROLLWALL_STATE)
			else:
				# test if finish rolling
				if (self.rig.getActionFrame(1) == 11):
					# change state
					self.switchState(PlayerState.IDLE_STATE)
		# else go t ojump like normal zelda game
		else:
			# change state
			self.switchState(PlayerState.JUMP_STATE)

def rollWallState(self):
	# test if finish rolling wall wanimation
	if (self.rig.getActionFrame(1) == 30):
		# change state
		self.switchState(PlayerState.IDLE_STATE)
	else:
		stop_rollWall_force(self)
