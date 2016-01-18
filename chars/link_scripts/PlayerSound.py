from bge import logic, types
import aud
import os
import bpy

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
sfxPath = bpy.path.abspath("//../audio/link_sfx/")
#
attackSound = [aud.Factory(sfxPath + "attack_1.wav"),
aud.Factory(sfxPath + "attack_2.wav"),
aud.Factory(sfxPath + "attack_2.wav")]

jumpSound = aud.Factory(sfxPath + "link_jump.wav")
hurtSound = aud.Factory(sfxPath + "hurt_3.wav")
bounceSound = aud.Factory(sfxPath + "bounceHit.wav")

def loadAudStep(field):
    return aud.Factory(sfxPath + "step_" + field + ".wav")

class PlayerSound:

    def __init__(self):
        self.field = "grass"
        self.lastFrame = 0
        self.lastVoiceFrame = 0

    def setField(self, field):
        if (self.field != field):
            self.field = field

    def playStepSound(self, current_frame, frames):
        for frame in frames:
            r = range(frame-1, frame+1)
            if ( (current_frame >= frame and current_frame <= frame+1) and self.lastFrame != frame):
                self.lastFrame = frame
                device.play(loadAudStep(self.field))

    def playAttack1Sound(self, current_frame, frame, index=0):
        if ( (current_frame >= frame and current_frame <= frame+1) and self.lastFrame != frame):
            self.lastFrame = frame
            device.play(attackSound[index])
        if (not (current_frame >= frame and current_frame <= frame+1) ):
            self.lastFrame = -1

    def playJumpSound(self):
        device.play(jumpSound)

    def playHurtSound(self):
        device.play(hurtSound)

    def playBounceSound(self):
        device.play(bounceSound)
