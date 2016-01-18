from bge import logic
from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Hits import start_hitState
from link_scripts.states.Roll import start_rollState
from link_scripts.states.Water import start_swimState
from link_scripts.StarterState import start_levelGapState, start_pathFollowState

def runForce(self, forward_force):
	self.linearVelocity[0] = 0
	self.linearVelocity[1] = forward_force
	if (self.linearVelocity[1] > 7.0):
		return True
	else:
		return False

def end_runState(self):
	# deactivate the arm rig layer
	self.rig.stopArmLayer()

def runState(self):
	#playerHUD = logic.playerHUD
	# get forward force
	forward_force = self.getForwardForce()

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
		# cancel method
	else:
		# if touch the ground ( else callback )
		if ( self.respectGroundRule(end_runState) ):
			# if detect next-level
			if (self.tester.switchLevel()):
				# End run state
				end_runState(self)
				# cancel state
				return
			# if arrow key is pressed
			elif ( forward_force != 0.0 ):
				# set action hud text
				#logic.playerHUD.changeActionText('Roll')
				# if push to action key
				if (self.gamepad.isActionPressed()):
				# NEXT STATE : ROLL
					# stop orientation
					self.orientManager.stopOrientation(self)
					# start roll
					start_rollState(self)
					# switch roll state
					self.switchState(PlayerState.ROLL_STATE)
				else:
					# run force
					if ( runForce(self, forward_force) ):
						# play run animation
						self.rig.playRun()
						# Arm Hunk Animation
						if (self.armed):
							# Run with sword and shield arm
							self.rig.playRunArmArmed()
						else:
							self.rig.playRunArmBase()
						# play with step sounds
						self.audio.playStepSound(self.rig.getActionFrame(1), [4, 11])
					else:
						# go to walk
						self.switchState(PlayerState.WALK_STATE)
					# active orientation movement
					self.orientManager.orient_player(self)
			# else not movement go idle state
			else:
				# reset hud action text
				#logic.playerHUD.resetActionText()
				# stop orientation
				self.rig.stopArmLayer()
				self.orientManager.stopOrientation(self)
				# go to idle state
				self.switchState(PlayerState.IDLE_STATE)
		# if dont touch the ground go to jump state
		else:
			# reset hud action text
			#logic.playerHUD.resetActionText()
			# stop orientation
			self.orientManager.stopOrientation(self)
			# go to idle state
			self.switchState(PlayerState.JUMP_STATE)
