from bge import logic
from link_scripts.PlayerConstants import PlayerState

def start_interactionState(self):
    self.switchState(PlayerState.DIALOGUE_INTERACTION_STATE)
    self.interaction.displayMessageInput()

def dialogueInteractionState(self):
    # if message finished
    if (logic.playerHUD.messageBox.active):
        # play wait animation
    	self.rig.playWait()
    else:
        # go t oidle State
        self.switchState(PlayerState.IDLE_STATE)
