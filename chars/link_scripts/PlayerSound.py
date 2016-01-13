from bge import logic, types
import aud
import os
import bpy

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
sfxPath = bpy.path.abspath("//../audio/link_sfx/")
#
attack_1 = aud.Factory(sfxPath + "attack_1.wav")

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

    def playAttack1Sound(self, current_frame, frame):
        if ( (current_frame >= frame and current_frame <= frame+1) and self.lastFrame != frame):
            self.lastFrame = frame
            device.play(attack_1)
        if (not (current_frame >= frame and current_frame <= frame+1) ):
            self.lastFrame = -1
