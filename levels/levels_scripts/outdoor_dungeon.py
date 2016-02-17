from bge import logic

scene = logic.getCurrentScene()

def chest(cont):
    own = cont.owner
    chest = scene.addObject("wood_chest", own)
    if ( logic.globalDict['Chests']['chest.basic_sword'] ):
        chest['alreadyOpen'] = True
    else:
        chest['objectID'] = 1
        chest['key'] = "chest.basic_sword"
    # end
    own.endObject()
