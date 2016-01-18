from bge import logic

def main(cont):
    own = cont.owner
    # add effect
    touchDamage = cont.sensors['touchDamage']
    if (touchDamage.positive and touchDamage.hitObject['damage'] > 0.0):
        cont.activate('addCutEffect')
        cont.activate('addCutGrass')
        own.endObject()
