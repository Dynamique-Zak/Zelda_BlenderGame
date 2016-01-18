from bge import logic
from link_scripts.PlayerConstants import PlayerState

scene = logic.getCurrentScene()
objects = scene.objects

# Utils
def hitEffect(self):
    effect = scene.addObject("strikeEffect1", self, 30)
    effect.scaling = [1.5, 1.5, 1.5]

    # change color to red
    objects['link_mesh'].color = [1, 0, 0, 1]
    # play hit sound
    #device.play(hitSound)

def restoreColor(self):
    objects['link_mesh'].color = [1, 1, 1, 1]

# Starters
def start_hitState(self):
    self.stopMovement()
    start_hitUpercut(self)

def start_hitUpercut(self):
    # Lose heart
    self.applyDamage()
    # Play animation
    self.rig.playHitUpercut()
    # Play sound
    self.audio.playHurtSound()
    # Hit effect
    hitEffect(self)
    # Deactive ground
    self.grounded = False
    # Fall up force
    self.linearVelocity[2] += 16.0
    self.linearVelocity[1] -= 8.0
    # Go to state
    self.switchState(PlayerState.HIT_UPERCUT_STATE)

def start_hitBounce(self):
    # Play animation
    self.rig.playHitBounce()
    # Sound
    self.audio.playBounceSound()
    # Reactive ground
    self.grounded = True
    # Stop movement
    self.stopMovement()
    # Go to state
    self.switchState(PlayerState.HIT_BOUNCE_STATE)

def start_bounceStandUp(self):
    # Play animation
    self.rig.playBounceStandUp()
    # Go to state
    self.switchState(PlayerState.BOUNCE_STANDUP_STATE)

def hitUpercutState(self):
    # if touch the ground
    if (self.tester.detectGround()):
        # go to bounce hit
        start_hitBounce(self)
    else:
        frame = self.rig.getActionFrame(5)
        if (frame >= 5):
            restoreColor(self)

def hitBounceState(self):
    frame = self.rig.getActionFrame(5)
    if ( frame == 32):
        # go to idle
        start_bounceStandUp(self)

def bounceStandUpState(self):
    frame = self.rig.getActionFrame(5)
    if ( frame == 46):
        # go to idle
        self.switchState(PlayerState.IDLE_STATE)
