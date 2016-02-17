from bge import logic
from link_scripts.PlayerConstants import *

scene = logic.getCurrentScene()

def start_pickObjectState(self):
    self.pickManager.active = True
    self.rig.pickAnimation = self.pickManager.pickedObject['pickable']
    self.switchState(PlayerState.PICK_OBJECT_STATE)

def start_throwObjectState(self):
    #self.rig.playThrow()
    self.switchState(PlayerState.THROW_OBJECT_STATE)

def pickObjectState(self):
    # play pick animation
    # to do

    # set pickable object to pickObjectPos
    pick_throw_obj = scene.objects["arm_obj"]
    self.pickManager.pickedObject.pick(pick_throw_obj)

    # go to idle states
    self.switchState(PlayerState.IDLE_STATE)

def throwObjectState(self):
    #if (self.rig.getActionFrame(10) == 6):
        # throw the object
    self.pickManager.pickedObject.throw()
    self.rig.pickAnimation = -1
    self.pickManager.active = False
    # go to idle
    self.switchState(PlayerState.IDLE_STATE)
