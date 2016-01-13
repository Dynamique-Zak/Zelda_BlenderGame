from bge import logic
from .monster import Monster

def init(cont):
    own = cont.owner
    Monster(own)
    own.state = 2+8
    
def main(cont):
    pass