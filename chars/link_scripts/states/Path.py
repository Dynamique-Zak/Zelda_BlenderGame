from bge import logic

from link_scripts.PlayerConstants import PlayerState
from link_scripts.StarterState import start_pathFollowLevelState

def start_pathFollowState(self):
	# cancel orientation
	self.orientManager.stopOrientation(self)
	nextStep(self)
	# deactivate track player cam
	self.camManager.deactiveTrackPlayer()
	self.camManager.activeLookPlayer()
	# swithc state
	self.switchState(PlayerState.PATH_FOLLOW_STATE)

def distPathTarget(self):
	dist = (self.trackTarget.position - self.position).length
	return dist

def nextStep(self):
	self.levelManager.step += 1
	find = False
	for obj in self.levelManager.pathObject.children:
		name = "path_step_" + str(self.levelManager.step)
		if (name in obj.name):
			# Orient to track
			self.orientManager.targetObject(obj)
			self.setTrackOrient(obj)
			find = True
	return find

def pathFollowState(self):
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
