# ==========================================================
# * Imports
# ==========================================================
# Import states
from link_scripts.states.Bow import *
from link_scripts.states.Death import *
from link_scripts.states.Chest import *
from link_scripts.states.Push import *
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

# Other Imports
from .PlayerConstants import PlayerState

# ==========================================================
# * State management
# ==========================================================
def managePlayerState(player):
	etat = player.etat

	# * Idle State
	if (etat == PlayerState.IDLE_STATE):
		idleState(player)

	# * Walk State
	elif (etat == PlayerState.WALK_STATE):
		walkState(player)

	# * Run State
	elif (etat == PlayerState.RUN_STATE):
		runState(player)
    # * Jump State
	elif (etat == PlayerState.JUMP_STATE):
		jumpState(player)

	# * Fall State
	elif (etat == PlayerState.FALL_STATE):
		fallState(player)

	# * Land State
	elif (etat == PlayerState.LAND_STATE):
		lowLandState(player)

	# * Roll State
	elif (etat == PlayerState.ROLL_STATE):
		 rollState(player)

	elif (etat == PlayerState.ROLLWALL_STATE):
		 rollWallState(player)

	# * Ledge State
	elif (etat == PlayerState.START_GRAPLEDGE_STATE):
		 startGrapLedgeState(player)

	elif (etat == PlayerState.BEGIN_GRAPLEDGE_STATE):
		 beginGrapLedgeState(player)

	elif (etat == PlayerState.GRAPLEDGE_STATE):
		grapLedgeState(player)

	elif (etat == PlayerState.CLIMBLEDGE_STATE):
		climbLedgeState(player)

	elif (etat == PlayerState.START_LADDER_TOP_STATE):
		 ladderTopState(player)

	# * Climb State
	elif ( etat == PlayerState.CLIMBGROUND_STATE):
		climbGroundState(player)

	# * Ladder State
	elif (etat == PlayerState.WAITLADDER_STATE):
		 waitLadderState(player)

	elif (etat == PlayerState.CLIMBUPLADDER_STATE):
		 climbUpLadderState(player)

	elif (etat == PlayerState.CLIMBDOWNLADDER_STATE):
		 climbDownLadderState(player)

	elif (etat == PlayerState.CLIMB_TO_GROUND_LADDER_STATE):
		 climbToGroundLadderState(player)

	# * Water state
	elif (etat == PlayerState.WAIT_SWIM_STATE):
		 waitSwimState(player)

	elif (etat == PlayerState.FORWARD_SWIM_STATE):
		forwardSwimState(player)

	# * Path State
	elif (etat == PlayerState.PATH_FOLLOW_STATE):
		pathFollowState(player)

	# * SwitchLevel State
	elif (etat == PlayerState.LEVEL_GAP_STATE):
		levelGapState(player)

	elif (etat == PlayerState.PATH_FOLLOW_LEVEL_STATE):
		levelPathFollowState(player)

	# * Look state
	elif (etat == PlayerState.FIRST_LOOK_VIEW_STATE):
		firstLookViewState(player)

	# * Targeting State
	elif (etat == PlayerState.IDLE_TARGET_STATE):
		idleTargetState(player)

	elif (etat == PlayerState.STRAFE_STATE):
		strafeState(player)

	elif (etat == PlayerState.LEFT_STRAFE_ROLL_STATE):
		leftStrafeRollState(player)

	elif (etat == PlayerState.RIGHT_STRAFE_ROLL_STATE):
		rightStrafeRollState(player)

	elif (etat == PlayerState.FALL_BACK_JUMP_STATE):
		fallBackJump(player)

	elif (etat == PlayerState.BOUNCE_BACK_JUMP_STATE):
		bounceBackJump(player)

	# * Attack state
	elif (etat == PlayerState.BASIC_SWORD_ATTACK_1_STATE):
		basicSwordAttack1State(player)

	elif (etat == PlayerState.BASIC_SWORD_ATTACK_2_STATE):
		basicSwordAttack2State(player)

	elif (etat == PlayerState.BASIC_SWORD_ATTACK_3_STATE):
		basicSwordAttack3State(player)

	elif (etat == PlayerState.BEGIN_JUMP_ATTACK_STATE):
		fallJumpAttackState(player)

	elif (etat == PlayerState.BOUNCE_JUMP_ATTACK_STATE):
		bounceJumpAttackState(player)

	elif (etat == PlayerState.CLANG_SWORD_STATE):
		clangSwordState(player)

	elif (etat == PlayerState.SPECIAL_ROLL_STATE):
		specialRollState(player)

	elif (etat == PlayerState.SPECIAL_ATTACK_1_STATE):
		specialAttack1State(player)

	# * Hits State
	elif (etat == PlayerState.HIT_UPERCUT_STATE):
		hitUpercutState(player)

	elif (etat == PlayerState.HIT_BOUNCE_STATE):
		hitBounceState(player)

	elif (etat == PlayerState.BOUNCE_STANDUP_STATE):
		bounceStandUpState(player)

	# * PickThrow State
	elif (etat == PlayerState.PICK_OBJECT_STATE):
		pickObjectState(player)

	elif (etat == PlayerState.THROW_OBJECT_STATE):
		throwObjectState(player)

	# * Interaction State
	elif (etat == PlayerState.DIALOGUE_INTERACTION_STATE):
		dialogueInteractionState(player)

	# * Door State
	elif (etat == PlayerState.OPEN_DOOR_STATE):
		openDoorState(player)

	elif (etat == PlayerState.RUN_AFTER_DOOR_STATE):
		runAfterDoorState(player)

	elif (etat == PlayerState.WAIT_PUSH_STATE):
		waitPushState(player)

	elif (etat == PlayerState.WALK_PUSH_STATE):
		walkPushState(player)

	elif (etat == PlayerState.OPENSMALL_CHEST_STATE):
		openSmallChestState(player)

	elif (etat == PlayerState.OPENBIG_CHEST_STATE):
		openBigChestState(player)

	elif (etat == PlayerState.WAITCONFIRM_CHEST_STATE):
		waitConfirmChestState(player)

	elif (etat == PlayerState.OPEN_CHEST_STATE):
		openChestState(player)

	elif (etat == PlayerState.GROUND_DEATH_STATE):
		groundDeathState(player)

	elif (etat == PlayerState.DIE_DEATH_STATE):
		DieDeathState(player)

	elif (etat == PlayerState.OPENSLIDE_DOOR_STATE):
		openSlideDoorState(player)

	elif (etat == PlayerState.AFTEROPEN_DOOR_STATE):
		afterOpenDoorState(player)

	elif (etat == PlayerState.UNLOCK_DOOR_STATE):
		unlockDoorState(player)

	elif (etat == PlayerState.GRAP_LEDGE_STATE):
		grapLedgeState(player)

	elif (etat == PlayerState.BEGINGRAP_LEDGE_STATE):
		beginGrapLedgeState(player)

	elif (etat == PlayerState.GOTOWAIT_LEDGE_STATE):
		goToWaitLedgeState(player)

	elif (etat == PlayerState.WAIT_LEDGE_STATE):
		waitLedgeState(player)

	elif (etat == PlayerState.CLIMB_LEDGE_STATE):
		climbLedgeState(player)

	elif (etat == PlayerState.FIRE_BOW_STATE):
		fireBowState(player)

	elif (etat == PlayerState.WAITSPINSWORD_ATTACK_STATE):
		waitSpinSwordAttackState(player)

	elif (etat == PlayerState.SPINSWORD_ATTACK_STATE):
		spinSwordAttackState(player)
	# * End State Management
