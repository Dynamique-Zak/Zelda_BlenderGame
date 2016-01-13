from bge import logic

def main(cont):
    own = cont.owner
    
    own.linearVelocity[1] = 0.0
    own.linearVelocity[0] = 0.0
    
    #active animation
    cont.activate('idle')