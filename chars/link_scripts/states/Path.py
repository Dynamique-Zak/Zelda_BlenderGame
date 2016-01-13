from link_scripts.PlayerConstants import PlayerState
from link_scripts.StarterState import start_pathFollowLevelState

def distPathTarget(self):
	dist = (self.trackTarget.position - self.position).length
	return dist

def nextStep(self):
	self.levelManager.step += 1
	find = False
	for obj in self.levelManager.pathObject.children:
		name = "path_step_" + str(self.levelManager.step)
		if (obj.name == name):
			self.setTrackOrient(obj)
			find = True
	return find

def pathFollowState(self):
	if (self.tester.detectNextLevelSwitcher()):
		start_pathFollowLevelState(self)
	else:
		# if near the target step change to the next step
		if ( distPathTarget(self) < 1.2):
			# change to the next step
			nextStep(self)
		else:
			# play run animation
			self.rig.playRun()
			# move
			self.linearVelocity[0] = 0
			self.linearVelocity[1] = 8.0
