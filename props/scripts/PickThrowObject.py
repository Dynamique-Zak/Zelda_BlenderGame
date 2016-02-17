from bge import types

class PickThrowObject(types.KX_GameObject):

    def __init__(self, own):
        self.etat = ""
        self.picked = False

    def pick(self, parent):
        self.suspendDynamics(True)
        self.worldPosition = parent.worldPosition
        self.orientation = parent.orientation
        self.setParent(parent)
        self.picked = True

    def end(self):
        self.endObject()

    def throw(self, throw_force = 0.0):
        self.removeParent()
        self.restoreDynamics()
        # Apply throw force
        if (throw_force > 0.0):
            self.linearVelocity[1] += throw_force
        self.picked = False
