from link_scripts.PlayerConstants import *

def start_basicSwordAttack1State(self):
    self.rig.playBasicSwordAttack1()
    self.switchState(PlayerState.BASIC_SWORD_ATTACK_1)

def start_basicSwordAttack2State(self):
    self.rig.playBasicSwordAttack2()
    self.switchState(PlayerState.BASIC_SWORD_ATTACK_2)


def finishAttack(self):
    if (self.targetManager.active):
        # go to idle target state
        self.switchState(PlayerState.IDLE_TARGET_STATE)
    else:
        # go to normal idle
        self.switchState(PlayerState.IDLE_STATE)

def basicSwordAttack1State(self):
    # IF fnish the sword attack
    frame = self.rig.getActionFrame(5)
    if ( frame == 9):
        finishAttack(self)
    else:
        self.audio.playAttack1Sound(frame, 2)
        if (frame >= 7.0):
            # next attack
            if ( self.gamepad.isAttackPressed() ):
                start_basicSwordAttack2State(self)
                return

def basicSwordAttack2State(self):
    # IF fnish the sword attack
    frame = self.rig.getActionFrame(5)
    if ( frame == 17):
        finishAttack(self)
    else:
        self.audio.playAttack1Sound(frame, 12)
