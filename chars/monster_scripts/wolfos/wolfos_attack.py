from bge import logic
from .wolfos_utils import *
from .wolfos_hit_test import *

def basic_attack(own, cont, left_box):
    frame = cont.actuators['attack_1'].frame
    own.linearVelocity[1] = 0.0
    #go to player
    if (frame >= 11):
        if (frame > 27.0):
            left_box['enemy_box_atk'] = False #stop attack
            own['attack'] = -1
            own['attack_left'] = 3
            own.state = logic.WOLFOS_FIGHT
        elif(frame <= 16):
            left_box['enemy_box_atk'] = True
            
            
def main(cont):
    own = cont.owner
    enemy = own['enemy']
    
    #go to hit
    if hit_test(own, cont):
        logic.WOLFOS_HIT
    #
    #Si le wolfos depasse la limite
    if limit_test(own, cont) :
        #go to reset
        own.state = logic.WOLFOS_RESET
        return
    
    if go_to_player(own, cont, own['enemy']):
        if (own['attack'] != 0):
            cont.activate('attack_1')
            cont.activate('slash')
            cont.actuators['attack_1'].frame = 0
            own['attack'] = 0
    else :
        if (own['attack'] < 0):
            if ("attack" in enemy["etat"]):
                own.state = logic.WOLFOS_GUARD
        
    if (own['attack'] == 0):
        basic_attack(own, cont, own['left_bound_atk'])