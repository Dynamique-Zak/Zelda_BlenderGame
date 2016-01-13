from link_scripts.PlayerConstants import PlayerState
from link_scripts.StarterState import start_pathFollowLevelState

def applyNewPosition(self):
	self.worldPosition[1] += 1.0

def openDoorState(self):
	# if anim finish ed
	if (self.rig.getActionFrame(5) == 48):
		# change pos
		applyNewPosition(self)
		# if detect new
		if (self.tester.detectNextLevelSwitcher()):
		  start_pathFollowLevelState(self)
		else:
		  # go to idle
		  self.switchState(PlayerState.IDLE_STATE)
