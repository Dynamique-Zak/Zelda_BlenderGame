from bge import logic
from .wolfos_utils import *

def main(cont):
    own = cont.owner
    own.linearVelocity[0] = 0.0
    if (go_to_point(own, cont)):
        own['attack'] = 3
        own['fight'] = False
        stop_target(cont)
        own.state = logic.WOLFOS_IDLE
    #