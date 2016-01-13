from bge import logic
from random import uniform

def random_orient(own):
    alpha = uniform(0, math.pi)
    own.worldOrientation = [0,0, alpha]