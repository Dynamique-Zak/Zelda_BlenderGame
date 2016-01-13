from bge import logic

def hit_fx(cont):
    cont.activate('hitX')
    cont.activate('hit')
    
def hit_small(own, cont, degats):
    hit_fx(cont)
    own['hp'] -= degats

def hit_test(own, cont):
    touch_sword = cont.sensors['touch_sword']
    
    if (touch_sword.positive) :
        box = touch_sword.hitObject
        if (box['attack_green']) :
            #HITTING
            own['degats'] = box['power']
            #sound
            return True
        else :
            return False
    else :
        return False

def main(cont):
    own = cont.owner
    
    hit_small(own, cont, degats)