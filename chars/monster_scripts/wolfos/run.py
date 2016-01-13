from bge import logic
from .wolfos_utils import step_run_sound
import math

def main(cont):
    own = cont.owner
    if (own['fight'] == True):
        if (own['axis'] == 0):
            own.linearVelocity[0] = 0.2
        elif (own['axis'] == 3):
            own.linearVelocity[0] = -0.2
    
    own.linearVelocity[1] = 5.0
    cont.activate('run')
    step_run_sound(cont)