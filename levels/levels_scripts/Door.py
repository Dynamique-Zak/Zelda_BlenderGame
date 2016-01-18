from bge import logic
import aud
import os
import bpy

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
sfxPath = bpy.path.abspath("//../audio/obj_sfx/")
#
doorOpenSound = aud.Factory(sfxPath + "door_mechanic_open.wav")
doorCloseSound = aud.Factory(sfxPath + "door_mechanic_close.wav")
doorBounceSound = aud.Factory(sfxPath + "door_bounce.wav")

# Constants
PLAY = logic.KX_ACTION_MODE_PLAY

def open(cont):
    own = cont.owner
    device.play(doorOpenSound)

def close(cont):
    own = cont.owner
    device.play(doorCloseSound)
