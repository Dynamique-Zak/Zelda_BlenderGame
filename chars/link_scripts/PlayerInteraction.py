from bge import logic
from hud_scripts.HUDConstant import MessageBoxMode

class PlayerInteraction:

    def __init__(self):
        self.message = ""

    def setMessage(self, message):
        self.message = message

    def displayMessage(self):
        logic.playerHUD.messageBox.displayText(self.message)

    def displayMessageInput(self):
        logic.playerHUD.messageBox.displayText(self.message, MessageBoxMode.WAIT_INPUT_TYPE)
