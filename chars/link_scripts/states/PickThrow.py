from bge import logic
from link_scripts.PlayerConstants import *

scene = logic.getCurrentScene()

def start_pickObjectState(self):
    self.onPick = True
    self.switchState(PlayerState.PICK_OBJECT_STATE)

def start_throwObjectState(self):
    self.rig.playThrow()
    self.switchState(PlayerState.THROW_OBJECT_STATE)

def pickObjectState(self):
    # play pick animation
    # to do

    # set pickable object to pickObjectPos
    pick_throw_obj = scene.objects["pick_throw_obj"]
    self.objectPickable.pick(pick_throw_obj)

    # go to idle states
    self.switchState(PlayerState.IDLE_STATE)

def throwObjectState(self):
    if (self.rig.getActionFrame(10) == 6):
        # throw the object
        self.objectPickable.throw()
        self.onPick = False
        # go to idle
        self.switchState(PlayerState.IDLE_STATE)
