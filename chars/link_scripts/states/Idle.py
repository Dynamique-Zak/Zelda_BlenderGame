from bge import logic
from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Attack import start_basicSwordAttack1State
from link_scripts.states.Interaction import start_interactionState
from link_scripts.states.PickThrow import start_pickObjectState, start_throwObjectState
from link_scripts.StarterState import start_firstLookView, start_openDoorState, start_ladderState

def idleState(self):
	# stop movement
	self.stopMovement()

	# play wait animation
	self.rig.playWait()

	# get forward force
	forward_force = self.getForwardForce()

	if (self.onPick == True):
		# if action pressed
		if ( self.gamepad.isAttackPressed() ):
			start_throwObjectState(self)
			return
		else:
			self.rig.playPick()

	# If detect pckable object
	if ( self.tester.detectObjectToPickUp() and self.onPick == False ):
		if (self.gamepad.isActionPressed() ):
			start_pickObjectState(self)
			return

	# test if detect placard
	if (self.tester.detectInteractivePlacard()):
		if ( self.gamepad.isActionPressed() ):
			start_interactionState(self)
			return

	# test if can target a object
	if ( self.targetManager.canTargetObject() ):
		self.switchState(PlayerState.IDLE_TARGET_STATE)
		return

	# if move go to walk animation
	if (forward_force != 0):
		if (self.targetManager.active):
			self.switchState(PlayerState.STRAFE_STATE)
		else:
			self.switchState(PlayerState.WALK_STATE)
	# other action
	else:
		# if detect key for look
		if ( self.gamepad.isLookPressed() ):
			# go to look state
			start_firstLookView(self)
		# detect lader
		elif (self.tester.detectLadder()):
			# change hud action text
			#self.playerHUD().changeActionText('Monter')
			if ( self.gamepad.isActionPressed() ):
				# go to ladder state
				start_ladderState(self)
		# detect a door
		elif (self.tester.detectDoor()):
			if ( self.gamepad.isActionPressed() ):
				# g oto ladder state
				start_openDoorState(self)
		# go to get armed
		elif (self.gamepad.isAttackPressed()):
			if (self.armed == False):
				# play get armed animation
				#self.rig.playGetArmed()
				# set to armed
				self.activeArmedMode()
			else:
				start_basicSwordAttack1State(self)
