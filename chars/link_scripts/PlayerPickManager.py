from bge import logic

class PlayerPickManager:

    def __init__(self, player):
        self.active = False
        self.player = player
        self.pickType = 0
        self.pickedObject = None

    def canAlwaysHold(self, function=None):
        if (self.active):
            can = True
            if (self.pickedObject.etat == "dead"):
                can = False

            # If can't
            if (can == False):
                obj = self.pickedObject
                self.active = False
                self.pickedObject = None
                self.player.rig.pickAnimation = -1
                # Call the end method to a pickable object
                obj.end()
                #  Callback if function arguments exists
                if (function != None):
                    function(self.player)
            return can
