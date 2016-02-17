from bge import logic, types
from scripts.PickThrowObject import *

class WoodStick(PickThrowObject):

    def __init__(self, own):
        PickThrowObject.__init__(self, own)
        self.fireOn = False

    def setFireVisible(self, state=True):
        for obj in self.children:
            if (obj.name == "woodStick_fire"):
                obj.setVisible(state, True)

    def offFire(self):
        if (self.fireOn == True):
            self.fireOn = False
            self.etat = "goToDead"

            # Create fire source property
            for obj in self.children:
                if "fireSource" in obj.name:
                    del obj['fireSource']

            return True
        else:
            return False

    def onFire(self):
        if (self.fireOn == False):
            self.fireOn = True
            self.setFireVisible()

            # Create fire source property
            for obj in self.children:
                if "fireSource" in obj.name:
                    obj['fireSource'] = True

            return True
        else:
            return False

    def dead(self):
        if (self.etat == "goToDead"):
            self.etat = "dead"
        # If the object was not picked destroy it
        if (self.picked == False):
            self.endObject()

def init(cont):
    own = cont.owner
    own = WoodStick(own)
    own.setFireVisible(False)
    own.state = 2

def onFire(cont):
    sens = cont.sensors['detectFire']
    obj = sens.hitObject
    if (obj['fireSource'] == True and cont.owner.onFire()):
        cont.activate('soundInitFire')
        cont.activate('activeFireSource')
        cont.owner['lifeTime'] = 0.0

def dead(cont):
    cont.owner.dead()

def main(cont):
    cont.owner['lifeTime'] += 0.03

    # Go to dead
    if (cont.owner['lifeTime'] > 20.0):
        if (cont.owner.offFire()):
            cont.activate('deactiveFireSource')
            cont.activate('goToOff')
