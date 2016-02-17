from bge import logic, types
import aud
import os
import bpy

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
sfxPath = bpy.path.abspath("//../audio/link_sfx/")
sfxPathOther = bpy.path.abspath("//../audio/other/")
#
attackSound = [aud.Factory(sfxPath + "attack_1.wav"),
aud.Factory(sfxPath + "attack_2.wav"),
aud.Factory(sfxPath + "attack_2.wav")]

jumpSound = aud.Factory(sfxPath + "link_jump.wav")
hurtSound = aud.Factory(sfxPath + "hurt_3.wav")
bounceSound = aud.Factory(sfxPath + "bounceHit.wav")
swordSwing = aud.Factory(sfxPath + "sword_swing.wav")

# INDEX

def loadAudStep(field):
    return aud.Factory(sfxPath + "step_" + field + ".wav")

class PlayerSoundConstant:
    HOT = 0
    PUSH = 1
    STEP_PUSH = 2
    FANFARE_ITEM = 3
    CHOKE = 4
    BOUNCE = 5
    GAME_OVER = 6
    CLIMB_LEDGE = 7
    GASP_LEDGE = 8

class PlayerSound:

    def __init__(self):
        self.field = "grass"
        self.lastFrame = 0
        self.lastFrameSwing = 0
        self.lastVoiceFrame = 0

        logic.playerAudioHandle = [None]

        logic.playerAudio = [aud.Factory(sfxPath + "hot.wav").loop(-1), aud.Factory(sfxPath + "link_push.wav"),
            aud.Factory(sfxPath + "steps_push_grass.wav"),
            aud.Factory(sfxPathOther + "fanfare_item.wav"),
            aud.Factory(sfxPath + "link_choke.wav"),
            aud.Factory(sfxPath + "bounceHit.wav"),
            aud.Factory(sfxPathOther + "game_over.mp3"),
            aud.Factory(sfxPath + "link_ledge_climb.wav"),
            aud.Factory(sfxPath + "link_ledge_fall.wav"),]

    def setField(self, field):
        if (self.field != field):
            self.field = field

    def playStepSound(self, current_frame, frames):
        for frame in frames:
            if ( (current_frame >= frame and current_frame <= frame+1) and self.lastFrame != frame):
                self.lastFrame = frame
                device.play(loadAudStep(self.field))

    def playFrameSound(self, current_frame, frames, audio):
        for frame in frames:
            if ( (current_frame >= frame and current_frame <= frame+1) and self.lastFrame != frame):
                self.lastFrame = frame
                # Play audio
                device.play(audio)

    def playAttack1Sound(self, current_frame, frame, index=0):
        if ( (current_frame >= frame and current_frame <= frame+1) and self.lastFrame != frame):
            self.lastFrame = frame
            device.play(attackSound[index])
        if (not (current_frame >= frame and current_frame <= frame+1) ):
            self.lastFrame = -1

    def playSoundSwingFrame(self, current_frame, frame, index=0):
        if ( (current_frame >= frame and current_frame <= frame+1) and self.lastFrameSwing != frame):
            self.lastFrameSwing = frame
            device.play(swordSwing)
        if (not (current_frame >= frame and current_frame <= frame+1) ):
            self.lastFrameSwing = -1

    def playJumpSound(self):
        device.play(jumpSound)

    def playHurtSound(self):
        device.play(hurtSound)

    def playBounceSound(self):
        device.play(bounceSound)

    def playSwordSwingSound(self):
        device.play(swordSwing)

    def getAudio(self, index):
        return logic.playerAudio[index]

    def playAudio(self, index, handle=False):
        if (handle):
            logic.playerAudioHandle[index] = device.play(logic.playerAudio[index])
        else:
            device.play(logic.playerAudio[index])
