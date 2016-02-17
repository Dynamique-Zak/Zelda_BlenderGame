#===================================================
# * Author : Schartier Isaac
# * Mail : schartier.isaac@gmail.com
# * Role : Project Manager
# * Created 05/02/16 at 10:43
#===================================================

# Import modules
from link_scripts.PlayerConstants import PlayerState
from bge import logic
from link_scripts.PlayerSound import PlayerSoundConstant
from link_scripts.PlayerCam import PlayerCamAnimation
from hud_scripts.HUDConstant import MessageBoxMode
# ---------------------------------------------------------------------
# * Starters
# ---------------------------------------------------------------------
def start_openChestState(self):
	"""
	Documentation
	"""
	self.suspendDynamics()
	self.switchState(PlayerState.OPEN_CHEST_STATE)

def start_waitConfirmChestState(self):
	"""
	Documentation
	"""
	obj = logic.globalDict['Objects'][self.targetObject['objectID']]
	message = obj['description2']
	obj_name = obj['id_obj']
	self.interaction.displayMessageInput(message)
	self.interaction.hud().messageBox.displayObject(obj_name)
	# Apply modification into inventory
	self.inventory.addObject(obj)
	# Switch state
	self.switchState(PlayerState.WAITCONFIRM_CHEST_STATE)

def start_openBigChestState(self):
	"""
	Documentation
	"""
	# Align to target object
	self.alignToTargetObject()
	# Play Animation
	self.rig.playOpenBigChest()
	# Open this chest
	self.targetObject["open"] = True
	self.switchState(PlayerState.OPENBIG_CHEST_STATE)

def start_openSmallChestState(self):
	"""
	Documentation
	"""
	# Align to target object
	self.alignToTargetObject()
	# Play Animation
	self.rig.playOpenSmallChest()
	# Open this chest
	self.targetObject["open"] = True
	self.switchState(PlayerState.OPENSMALL_CHEST_STATE)

# ---------------------------------------------------------------------
# * Ending
# ---------------------------------------------------------------------
def end_chestState(self):
	self.restoreDynamics()
	scene = self.scene
	scene.active_camera = self.camManager.cam
	self.camManager.deactivateCamAnimation()
	self.switchState(PlayerState.IDLE_STATE)

# ---------------------------------------------------------------------
# * States
# ---------------------------------------------------------------------
def openChestState(self):
	"""
	Documentation
	"""
	if self.targetObject['type'] == 1:
		start_openBigChestState(self)
	else:
		start_openSmallChestState(self)

def waitConfirmChestState(self):
	"""
	Documentation
	"""
	# if message finished
	if (not logic.playerHUD.messageBox.active):
		self.interaction.hud().messageBox.removeObject()
		self.targetObject['finish'] = True
		end_chestState(self)

def openBigChestState(self):
	"""
	Documentation
	"""
	if ( not self.rig.isPlayingAction(5) ):
		# Set message box
		start_waitConfirmChestState(self)

def openSmallChestState(self):
	"""
	Documentation
	"""
	if ( not self.rig.isPlayingAction(5) ):
		# Set message box
		self.audio.playAudio(PlayerSoundConstant.FANFARE_ITEM)
		start_waitConfirmChestState(self)
	else:
		if (self.rig.getActionFrame(5) >= 29):
			# Active cam animation
			self.camManager.activeCamAnimation(PlayerCamAnimation.GET_ITEM)
