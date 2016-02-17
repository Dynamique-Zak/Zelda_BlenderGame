from bge import logic
from link_scripts.PlayerConstants import ObjectType
from link_scripts.states.Look import start_firstLookView

scene = logic.getCurrentScene()

class PlayerObjectManager:

    def __init__(self, player):
        self.player = player
        self.mode = ObjectType.BOW
        self.use = False

    def useObject(self):
        if (self.player.gamepad.isItemXPressed()):
            self.use = True
            # For test go to bow
            start_firstLookView(self.player)
