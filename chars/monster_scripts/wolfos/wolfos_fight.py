from bge import logic, types
from random import randint
from .wolfos_utils import *
from .wolfos_hit_test import *

def run_lat(own):
    own.state = logic.WOLFOS_RUN_LAT

def guard(own):
    own['axis'] = 1
    own.state = logic.WOLFOS_GUARD

def attack(own):
    own['axis'] = 1
    own.state = logic.WOLFOS_ATTACK
    
def main(cont):
    own = cont.owner
    
    enemy = own['enemy']
    detect = cont.sensors['detect_player']
    player = detect.hitObject
    #cont.activate('lookHead')
    
    #go to hit
    if hit_test(own, cont):
        logic.WOLFOS_HIT
        
    #if always on fight mode
    if ( not detect.positive):
        own['fight'] = False
        if( go_to_point(own, cont)):
            own.state = logic.WOLFOS_IDLE
            return
        else :
            own.state = logic.WOLFOS_IDLE
            return
    #0 mode to right, 1 to left 2 to back 3 to up ; 4 guard; 5 idle; 6 attack
    
    time = own['state_time']
    
    #Si le wolfos depasse la limite
    if limit_test(own, cont) :
        #go to reset
        own.state = logic.WOLFOS_RESET
        return
        
    #Si l'enemie est bien sur le sol
    if (detect_empty_space(own, cont)):
        if (time >= 1.0 or own['first_time']):
            state = randint(0,2)
            
            #delet first time
            if (own['first_time']):
                own['first_time'] = False
                    
            #SI le joueur attaque
            if ("attack" in enemy['etat']):
                guard(own)
            
            #SI le jouer est inactif    
            elif ("idle" in enemy['etat'] and (own['attack_left'] < 1)):
                attack(own)
            #SI le jouer est en mouvement
            elif (enemy.linearVelocity[0] != 0 or enemy.linearVelocity[1] != 0):
                    if (state == 0):
                        #track to x neg
                        own['axis'] = 0
                        run_lat(own)
                    elif (state == 1):
                        #track to x pos
                        own['axis'] = 3
                        run_lat(own)
                        
                    elif (state == 2):#idle
                        own['axis'] = 1
                        own.state = logic.WOLFOS_IDLE_FIGHT
                    
             #AU PIRE DES CAS    
            else:
                own['axis'] = 1
                own.state = logic.WOLFOS_IDLE_FIGHT
                
            #own['state_time']
            target(cont, enemy, own['axis'])
            own['attack_left'] -= 1
            own['state_time'] = 0.0
            
    #EN L'AIR OU DETECT LE VIDE
    else :
        #go to reset
        own.state = logic.WOLFOS_RESET