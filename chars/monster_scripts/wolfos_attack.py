from bge import logic

def basic_attack(own, cont, left_box):
    frame = cont.actuators['attack_1'].frame
    
    if (frame >= 11):
        if (frame >= 16.0):
            left_box['enemy_box_atk'] = True
        else:
            left_box['enemy_box_atk'] = False #stop attack
            own['attack'] = -1
            own.state = logic.WOLFOS_IDLE_FIGHT
            
def main(cont):
    own = cont.owner
    
    if (own['attack'] != 0):
        cont.activate('attack_1')
        cont.activate('slash')
        own['attack'] = 0
        basic_attack(own, cont, own['left_bound_atk'])