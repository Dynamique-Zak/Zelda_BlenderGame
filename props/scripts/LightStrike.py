from bge import logic

scene = logic.getCurrentScene()

def main(cont):
    own = cont.owner # Is a KX_LightObject

    if ( own.energy < 3.0 and own['max'] == False ):
        own.energy += 0.5

    if ( own.energy >= 3.0 and own['max'] == False ):
        own['max'] = True

    if( own['max'] ):
        if (own.energy - 0.5 > 0.0):
            own.energy -= 0.5
        else:
            own.energy = 0.0
