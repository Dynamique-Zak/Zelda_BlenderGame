from bge import logic

def levelPathFollowState(self):
	self.levelManager.transitionTime += 0.1
	
	if ( self.levelManager.transitionIsFinish(4.5) ):
		# switch state to next level
	   self.levelManager.changeLevel()

def levelGapState(self):
	self.levelManager.transitionTime += 0.1
	
	if ( self.levelManager.transitionIsFinish(10.0) ):
		# switch state to next level
	   self.levelManager.changeLevel()
	else:
		if ( self.levelManager.transitionIsFinish(5.0) ):
			# hud transition
			logic.globalDict['PlayerHUD'].fadeOutToDisplayTransition()
			# deactive look
			self.camManager.deactiveLookPlayer()
		if (self.linearVelocity[2] <= 0.0):
			self.suspendDynamics()
			self.worldPosition[2] -= 0.1
			