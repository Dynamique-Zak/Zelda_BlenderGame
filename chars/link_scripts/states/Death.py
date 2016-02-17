#===================================================
# * Author : Schartier Isaac
# * Mail : schartier.isaac@gmail.com
# * Role : Project Manager
# * Created 12/02/16 at 20:09
#===================================================

# Import modules
from link_scripts.PlayerConstants import PlayerState
from bge import logic, render
from link_scripts.PlayerSound import PlayerSoundConstant
from link_scripts.PlayerCam import PlayerCamAnimation
# ---------------------------------------------------------------------
# * Starters
# ---------------------------------------------------------------------
def start_DieDeathState(self):
	"""
	Documentation
	"""
	# Deactive physic
	self.suspendDynamics()
	# Play choke audio
	self.audio.playAudio(PlayerSoundConstant.CHOKE)
	self.audio.playAudio(PlayerSoundConstant.GAME_OVER)
	# Active cam animation
	self.camManager.activeCamAnimation(PlayerCamAnimation.DEATH)
	# Change ambiance
	scene = logic.getCurrentScene()
	scene.world.backgroundColor = [0,0,0]
	scene.world.ambientColor = [0.0, 0.0 ,0.0]
	scene.world.mistColor = [0.0, 0.0 ,0.0]
	scene.world.mistStart = 1.0
	scene.world.mistDistance = 5.0
	# Low health sound stop
	logic.playerHUD.low_healt(False)
	# Go to die state
	self.switchState(PlayerState.DIE_DEATH_STATE)

def start_groundDeathState(self):
	"""
	Documentation
	"""
	# Play Death animation
	self.rig.playGroundDeath()
	# go to death state
	self.switchState(PlayerState.GROUND_DEATH_STATE)

# ---------------------------------------------------------------------
# * States
# ---------------------------------------------------------------------
def DieDeathState(self):
	"""
	Documentation
	"""
	# Remove HUD
	scenes = logic.getSceneList()

	for i in scenes:
		if i.name == "HUD":
			i.end()
	# Die
	start_groundDeathState(self)

def groundDeathState(self):
	"""
	Documentation
	"""
	if ( not self.rig.isPlayingAction(5)):
		scene = logic.getCurrentScene()
		scene.suspend()
		# add game over scene
		logic.addScene("GameOver", 1)
	else:
		frame = self.rig.getActionFrame(5)
		audio = self.audio.getAudio(PlayerSoundConstant.BOUNCE)
		self.audio.playFrameSound(frame, [46], audio)
