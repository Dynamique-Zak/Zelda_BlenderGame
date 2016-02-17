from bge import logic
from random import randint

scene = logic.getCurrentScene()

def addRandomCrops(own):
    # Add random crops objects
    rand = randint(0,9)
    obj = ""
    # Test random
    if (rand == 2):
        obj = "green_rupee"
    elif (rand == 3 ):
        obj = "heart"
    # Add selected object in scene
    if (obj != ""):
        rupee = scene.addObject(obj, own, 2000)
        rupee.worldPosition[2] += 1.0
        rupee['dynamics'] = True


def main(cont):
    own = cont.owner
    # add effect
    touchDamage = cont.sensors['touchDamage']
    if (touchDamage.positive and touchDamage.hitObject['damage'] > 0.0):
        cont.activate('addCutEffect')
        cont.activate('addCutGrass')
        # Add random crops objects
        addRandomCrops(own)
        # End object
        own.endObject()
