from bge import types

class Bloc(types.KX_GameObject):

    def __init__(self, own):
        self.etat = ""
        self.blocked = False

    def block(self):
        self.blocked = True
        
    def isBlocked(self):
        return self.blocked

# Initialization
def init(cont):
    own = cont.owner
    own = Bloc(own)
