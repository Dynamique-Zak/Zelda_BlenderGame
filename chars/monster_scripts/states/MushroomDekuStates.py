from bge import logic
import aud
import os
import bpy

scene = logic.getCurrentScene()

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
sfxPath = bpy.path.abspath("//../audio/monster/")
#
hitSound = aud.Factory(sfxPath + "enemy_hit.wav")
bounceSound = aud.Factory(sfxPath + "enemy_bounce.wav")

# States
SLEEP_STATE = 0
IDLE_STATE = 1
RUN_STATE = 2
HIT_STATE = 3
LAST_HIT_STATE = 4
APPEAR_STATE = 5
DEAD_STATE = 6
ATTACK_STATE = 7

def hitMove(self):
    self.linearVelocity[0] = 0
    self.linearVelocity[1] = -4.5 - (self.shufferedDamage * 4.0)

def hitEffect(self):
    effect = scene.addObject("strikeEffect1", self, 30)
    size = self.shufferedDamage * 2.0
    effect.scaling = [size, size, size]
    # change color to red
    self.meshMonster.color = [1, 0, 0, 1]
    # play hit sound
    device.play(hitSound)

def restoreColor(self):
    self.meshMonster.color = [1, 1, 1, 1]

def startSleepState(self):
    self.suspendDynamics()
    self.switchState(SLEEP_STATE)

def startAppearState(self):
    self.playAppear()
    self.switchState(APPEAR_STATE)

def startAttackState(self):
    self.playAttack()
    self.switchState(ATTACK_STATE)

def startHitState(self):
    # Apply damage
    self.damage(self.shufferedDamage)
    # If is dead after damage go to the last hit
    if ( self.isDead() ):
        startLastHitState(self)
    # Else apply normal hit
    else:
        self.rig.stopAction(0)
        hitEffect(self)
        self.playHit()
        self.switchState(HIT_STATE)

def startLastHitState(self):
    self.suspendDynamics()
    self.rig.stopAction(0)
    hitEffect(self)
    self.playLastHit()
    self.switchState(LAST_HIT_STATE)

def startDeadState(self):
    self.switchState(DEAD_STATE)

def sleepState(self):
    self.stopMovement()

    if ( self.detectPlayer() ):
        startAppearState(self)
        self.targetMode = True
    else:
        # Play animation
        self.playSleep()

def appearState(self):
    self.stopMovement()
    # if finish th apparition
    frame = self.rig.getActionFrame(0)
    if ( frame == 169):
        # finish and go to idle
        self.switchState(IDLE_STATE)

def idleState(self):
    self.stopMovement()
    # Play animation
    self.playIdle()
    if ( not self.detectDamage(startHitState) ):
        distance = self.getDistanceTo(self.targetObject)
        if (self.targetMode and distance < 3.0):
            # Reaction delay
            if (self.isReactif(2.6)):
                self.trackTo(self.targetObject)
                if ( distance <= 2.0):
                    # Randint for attack
                    rand = self.generateRandomState(4)
                    if (rand > 1):
                        startAttackState(self)
        else:
            # to do
            pass

def runState(self):
    pass

def attackState(self):
    frame = self.rig.getActionFrame(0)
    if (frame == 66):
        self.trackTo(self.targetObject)
        self.switchState(IDLE_STATE)
    else:
        if (frame >= 39 and frame <= 42):
            self.trackTo(None)

        if (frame > 42 and frame < 47):
            self.setAttack(0.5)
        if (frame >= 47):
            self.setAttack(0)
            self.detectDamage(startHitState)

def hitState(self):
    self.trackTo(None)
    frame = self.rig.getActionFrame(0)
    # if finish
    if (frame == 21):
        self.switchState(IDLE_STATE)
    elif (frame >= 6):
        restoreColor(self)

    if (frame <= 4.0):
        hitMove(self)
    else:
        self.stopMovement()

    # If can re hit
    if (frame >= 10):
        self.detectDamage(startHitState)

def lastHitState(self):
    self.trackTo(None)
    frame = self.rig.getActionFrame(0)
    # If finish
    if (frame == 70):
        # go to dead
        startDeadState(self)
    elif (frame >= 40):
        restoreColor(self)
        if (frame >= 48 and self.unusedVar == False):
            self.unusedVar = True
            # play hit sound
            device.play(bounceSound)

def deadState(self):
    # Dead
    self.endObject()

def statesManager(self):
    etat = self.etat
    if (etat == SLEEP_STATE):
        sleepState(self)

    elif (etat == APPEAR_STATE):
        appearState(self)

    elif (etat == IDLE_STATE):
        idleState(self)

    elif (etat == RUN_STATE):
        runState(self)

    elif (etat == ATTACK_STATE):
        attackState(self)

    elif (etat == HIT_STATE):
        hitState(self)

    elif (etat == LAST_HIT_STATE):
        lastHitState(self)

    elif (etat == DEAD_STATE):
        deadState(self)
