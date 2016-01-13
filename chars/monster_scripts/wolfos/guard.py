from bge import logic

def main(cont):
    own = cont.owner
    
    own.linearVelocity[0] = 0.0
    own.linearVelocity[1] = 0.0
    
    cont.activate('guard')