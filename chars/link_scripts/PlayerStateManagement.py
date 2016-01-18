# import states
from link_scripts.states.Attack import *
from link_scripts.states.Climb import *
from link_scripts.states.Idle import *
from link_scripts.states.Door import *
from link_scripts.states.Fall import *
from link_scripts.states.Hits import *
from link_scripts.states.Jump import *
from link_scripts.states.SwitchLevel import *
from link_scripts.states.Walk import *
from link_scripts.states.Run import *
from link_scripts.states.Roll import *
from link_scripts.states.Path import *
from link_scripts.states.PickThrow import *
from link_scripts.states.Interaction import *
from link_scripts.states.Land import *
from link_scripts.states.Ladder import *
from link_scripts.states.Ledge import *
from link_scripts.states.Look import *
from link_scripts.states.Water import *
from link_scripts.states.Targeting import *

# Other
from .PlayerConstants import PlayerState

#PlayerState = PlayerClass.PlayerState

def managePlayerState(player):
	etat = player.etat
	# Idle state
	if (player.etat == PlayerState.IDLE_STATE):
		idleState(player)
	# Walk state
	elif (player.etat == PlayerState.WALK_STATE):
		walkState(player)
	# Run state
	elif (player.etat == PlayerState.RUN_STATE):
		runState(player)
   # Jump state
	elif (player.etat == PlayerState.JUMP_STATE):
		jumpState(player)
	# Fall state
	elif (player.etat == PlayerState.FALL_STATE):
		fallState(player)
	# Land state
	elif (player.etat == PlayerState.LAND_STATE):
		lowLandState(player)
	# Roll state
	elif (player.etat == PlayerState.ROLL_STATE):
		 rollState(player)
	# Collide the wall during a roll
	elif (player.etat == PlayerState.ROLLWALL_STATE):
		 rollWallState(player)

	#  ========================================================
	#  * CLIMB STATE PART
	#  ========================================================

	# When started to grap ledge
	elif (player.etat == PlayerState.START_GRAPLEDGE_STATE):
		 startGrapLedgeState(player)
	# when started to grap ledge 2
	elif (player.etat == PlayerState.BEGIN_GRAPLEDGE_TO_GROUND_STATE):
		 beginGrapLedgeToGround(player)
	# Grapeledge state
	elif (player.etat == PlayerState.GRAPLEDGE_STATE):
		grapLedgeState(player)
   # Climb ledge state
	elif (player.etat == PlayerState.CLIMBLEDGE_STATE):
		climbLedgeState(player)

	elif ( etat == PlayerState.CLIMBGROUND_STATE):
		climbGroundState(player)
#   # Wait to push a bloc state
#   elif (player.etat == PlayerState.WAITBLOC_STATE):
#   player.waitBlocState()
#   # Push bloc state
#   elif (player.etat == PlayerState.PUSHBLOCK_STATE):
#   player.pushBlocState()
	# Wait ladder state
	elif (player.etat == PlayerState.WAITLADDER_STATE):
		 waitLadderState(player)
	# Climb ladder to up state
	elif (player.etat == PlayerState.CLIMBUPLADDER_STATE):
		 climbUpLadderState(player)
	# Climb ladder to down state
	elif (player.etat == PlayerState.CLIMBDOWNLADDER_STATE):
		 climbDownLadderState(player)
	# Clim to ground from ladder
	elif (player.etat == PlayerState.CLIMB_TO_GROUND_LADDER_STATE):
		 climbToGroundLadderState(player)
	# Wait swim state
	elif (player.etat == PlayerState.WAIT_SWIM_STATE):
		 waitSwimState(player)
	# Forward swim state
	elif (player.etat == PlayerState.FORWARD_SWIM_STATE):
		forwardSwimState(player)
	# Path follow
	elif (player.etat == PlayerState.PATH_FOLLOW_STATE):
		pathFollowState(player)
	elif (player.etat == PlayerState.LEVEL_GAP_STATE):
		levelGapState(player)
	# path follow level
	elif (player.etat == PlayerState.PATH_FOLLOW_LEVEL_STATE):
		levelPathFollowState(player)
	# First person look view state
	elif (player.etat == PlayerState.FIRST_LOOK_VIEW_STATE):
		firstLookViewState(player)

	#  ========================================================
	#  * TARGET STATE PART
	#  ========================================================
	# idle target state
	elif (etat == PlayerState.IDLE_TARGET_STATE):
		idleTargetState(player)
	# strafeState
	elif (etat == PlayerState.STRAFE_STATE):
		strafeState(player)

	elif (etat == PlayerState.LEFT_STRAFE_ROLL_STATE):
		leftStrafeRollState(player)

	elif (etat == PlayerState.RIGHT_STRAFE_ROLL_STATE):
		rightStrafeRollState(player)

	elif (etat == PlayerState.FALL_BACK_JUMP):
		fallBackJump(player)

	elif (etat == PlayerState.BOUNCE_BACK_JUMP):
		bounceBackJump(player)

	#  ========================================================
	#  * ATTACK STATE PART
	#  ========================================================
	elif (etat == PlayerState.BASIC_SWORD_ATTACK_1):
		basicSwordAttack1State(player)

	elif (etat == PlayerState.BASIC_SWORD_ATTACK_2):
		basicSwordAttack2State(player)

	elif (etat == PlayerState.BASIC_SWORD_ATTACK_3):
		basicSwordAttack3State(player)

	elif (etat == PlayerState.BEGIN_JUMP_ATTACK):
		fallJumpAttackState(player)

	elif (etat == PlayerState.BOUNCE_JUMP_ATTACK):
		bounceJumpAttackState(player)

	#  ========================================================
	#  * HITS STATE PART
	#  ========================================================
	elif (etat == PlayerState.HIT_UPERCUT_STATE):
		hitUpercutState(player)

	elif (etat == PlayerState.HIT_BOUNCE_STATE):
		hitBounceState(player)

	elif (etat == PlayerState.BOUNCE_STANDUP_STATE):
		bounceStandUpState(player)

	#  ========================================================
	#  * PICK AND THROW STATE PART
	#  ========================================================
	elif (etat == PlayerState.PICK_OBJECT_STATE):
		pickObjectState(player)

	elif (etat == PlayerState.THROW_OBJECT_STATE):
		throwObjectState(player)

	#  ========================================================
	#  * INTERACTION PART
	#  ========================================================
	elif (etat == PlayerState.DIALOGUE_INTERACTION_STATE):
		dialogueInteractionState(player)

	# Open doot state
	elif (player.etat == PlayerState.OPEN_DOOR_STATE):
		openDoorState(player)

	elif (player.etat == PlayerState.RUN_AFTER_DOOR_STATE):
		runAfterDoorState(player)
