from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Ladder import start_ladderFromTop
from link_scripts.states.Hits import start_hitState
from link_scripts.StarterState import start_fallState
from link_scripts.states.Water import start_swimState

def walkForce(self, forward_force):
	self.linearVelocity[0] = 0
	self.linearVelocity[1] = forward_force
	if (self.linearVelocity[1] > 7.0):
		return True
	else:
		return False

def end_walkState(self):
	# deactivate the arm rig layer
	self.rig.stopArmLayer()

def walkState(self):
	# get forward force
	forward_force = self.getForwardForce()
	speedAnim = 1.0#abs(self.gamepad.getJoyAxis1Value())

	if (self.tester.detectLadderBottom()):
		start_ladderFromTop(self)
		return

	# If detect enemy damage
	if (self.tester.detectEnemyDamage()):
		start_hitState(self)
		return

	# If detect water
	if (self.tester.detectWater()):
		# stop orientation
		self.orientManager.stopOrientation(self)
		# start swim state
		start_swimState(self)
	# else we can move or wait
	elif ( self.respectGroundRule(end_walkState(self)) ):
		if (self.tester.switchLevel()):
			# cancel state
			return
		# if arrow key is pressed
		if (forward_force != 0.0):
			# use walk movement
			if walkForce(self, forward_force):
				# stop orientation
				self.orientManager.stopOrientation(self)
				# go to idle state
				self.switchState(PlayerState.RUN_STATE)
			else:
				# play walk animation
				self.rig.playWalk(speedAnim)
				# play step sound
				self.audio.playStepSound(self.rig.getActionFrame(1), [4, 13])
				# active orientation movement
				self.orientManager.orient_player(self)
		else:
			# stop orientation
			self.orientManager.stopOrientation(self)
			# go to idle state
			self.switchState(PlayerState.IDLE_STATE)
	# go to fall
	else:
		# go to fall state
		start_fallState(self)
