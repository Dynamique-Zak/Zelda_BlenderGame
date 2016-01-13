from bge import logic
from random import randint, uniform
import math
from .wolfos_utils import *
from .wolfos_hit_test import *

scene = logic.getCurrentScene()

def init(cont):
    own = cont.owner
    own['zone'] = scene.objects['monster_01_zone']
    own['arm'] = cont.sensors['arm_sens'].owner
    own['left_bound_atk'] = cont.sensors['lba_sens'].owner
    own['axis'] = 1
    own['enemy'] = None
    own['start_point'] = [own.worldPosition[0], own.worldPosition[1]]
    own['start_point_obj'] = cont.sensors['start_point_sens'].owner
    own['reset'] = False
    
    own['first_time'] = True
    
    own['hp'] = 3.0
    own['degats'] = 0.0
    
    #init state
    logic.WOLFOS_IDLE = 2 + 8
    logic.WOLFOS_RUN = 2 + 16
    logic.WOLFOS_IDLE_FIGHT = 32768 + 8
    logic.WOLFOS_FIGHT = 2 + 32768
    logic.WOLFOS_GUARD = 2 + 32768 + 32
    logic.WOLFOS_RUN_LAT = 32786
    logic.WOLFOS_ATTACK = 256
    logic.WOLFOS_RESET = 512
    logic.WOLFOS_HIT = 128
    #go to idle
    own.state = logic.WOLFOS_IDLE

#random orient
def random_orient(own):
    alpha = uniform(-math.pi, math.pi)
    own.worldOrientation = [0,0, alpha]
    
def idle_state(own):
    own.state = logic.WOLFOS_IDLE
    
def run_state(own):
    random_orient(own)
    own.state = logic.WOLFOS_RUN

def fight_state(own):
    own.state = logic.WOLFOS_FIGHT
    
def change_state(own, state):
    if (state == 0):
        idle_state(own)
    elif (state == 1):
        run_state(own)
    
def main(cont):
    own = cont.owner
    detect = cont.sensors['detect_player']
    
    #
    #go to hit
    if hit_test(own, cont):
        logic.WOLFOS_HIT
    
    #Si le wolfos depasse la limite
    if limit_test(own, cont) :
        #go to reset
        own.state = logic.WOLFOS_RESET
        return
    
    #Si l'enemie est bien sur le sol
    if (detect_empty_space(own, cont)):
        if (own['fight'] != True):
            rand_state = 0
            old = own['old_state']
            time = own['state_time']
            
            # IF DETECT PLAYER
            if (detect.positive):
                own['enemy'] = detect.hitObject
                #own['state_time'] = 0.0
                own['fight'] = True
                fight_state(own)
                return
            
            if (time >= 1.0):
                rand_state = randint(0,1)
                own['state_time'] = 0.0
                
                #delet first time
                if (own['first_time']):
                    own['first_time'] = False
                #change state
                if (old != rand_state):
                    own['old_state'] = rand_state
                    change_state(own, rand_state)
            else :
                if (own['first_time']):
                    change_state(own, 0)
    #EN L'AIR OU DETECT LE VIDE
    else :
        #go to reset
        own.state = logic.WOLFOS_RESET
        return