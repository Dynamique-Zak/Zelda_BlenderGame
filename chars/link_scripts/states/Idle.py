from bge import logic
from link_scripts.PlayerConstants import PlayerState
from link_scripts.states.Attack import start_basicSwordAttack1State
from link_scripts.states.Ledge import start_climbLedgeState
from link_scripts.states.Door import start_openDoorState
from link_scripts.states.Hits import start_hitState
from link_scripts.states.Interaction import start_interactionState
from link_scripts.states.PickThrow import start_pickObjectState, start_throwObjectState
from link_scripts.states.Push import start_waitPushState
from link_scripts.states.Chest import start_openChestState
from link_scripts.StarterState import start_firstLookView, start_ladderState

JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED

def idleState(self):
	# stop movement
	self.stopMovement()

	# play wait animation
	if (self.heartContainer.isLow):
		self.rig.playHeavyWait()
	else:
		self.rig.playWait()

	# get forward force
	forward_force = self.getForwardForce()

	# If use object
	if (self.objectManager.useObject()):
		return

	# If detect enemy damage
	if (self.tester.detectEnemyDamage()):
		start_hitState(self)
		return

	# If statetime is finish can do action
	if (self.playStateTime(1.0)):
		# If detect chest
		if ( self.tester.detectChest() ):
			if ( self.gamepad.isActionPressed() ):
				start_openChestState(self)
		# If detect bloc
		if (self.tester.detectBloc()):
			if (self.gamepad.isActionPressed()):
				start_waitPushState(self)
				return

		# If detect ledge ground from ground
		if (self.tester.detectLedgeGroundFromGround()):
			if (self.gamepad.isActionPressed()):
				# go to climb
				start_climbLedgeState(self)
				return

		# If detect pckable object
		if ( self.tester.detectObjectToPickUp() and self.pickManager.active == False ):
			if (self.gamepad.isActionPressed() ):
				start_pickObjectState(self)
				return

		# test if detect placard
		if (self.tester.detectInteractivePlacard()):
			if ( self.gamepad.isActionPressed(JUST_ACTIVATED) ):
				start_interactionState(self)
				return

	if (self.pickManager.active == True):
		# if action pressed
		if ( self.gamepad.isAttackPressed(JUST_ACTIVATED) ):
			start_throwObjectState(self)
			return

	# test if can target a object
	if ( self.targetManager.zTarget() ):#canTargetObject()
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

		# detect ladder
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
		elif (self.gamepad.isAttackPressed() and self.fightManager.canUseSword()):
			if (self.fightManager.isUnsheated() ):
				start_basicSwordAttack1State(self)
			else:
				self.unsheat(True)
		# range sword an shield
		if ( self.fightManager.isUnsheated() ):
			if ( self.gamepad.isActionPressed() ):
				self.unsheat(False)
