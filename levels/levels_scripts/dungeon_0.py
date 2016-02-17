from bge import logic

scene = logic.getCurrentScene()

def big_chest(own, obj, key):
    chest = scene.addObject("wood_chest", own)
    if ( key in logic.globalDict['Chests'] and logic.globalDict['Chests'][key] ):
        chest['alreadyOpen'] = True
    else:
        chest['objectID'] = obj
        chest['key'] = key

def small_chest(own, obj, key):
    chest = scene.addObject("small_chest", own)
    if ( key in logic.globalDict['Chests'] and logic.globalDict['Chests'][key] ):
        chest['alreadyOpen'] = True
    else:
        chest['objectID'] = obj
        chest['key'] = key
    return chest

def chest(cont):
    """ Wood shield chest """
    own = cont.owner
    big_chest(own, logic.OBJECT_CONSTANT.WOOD_SHIELD, "chest.wood_shield")
    # end
    own.endObject()

def chest_rupee(cont):
    """ Rupee chest """
    own = cont.owner
    small_chest(own, logic.OBJECT_CONSTANT.RUPEE, "chest.rupee")
    # end
    own.endObject()

def chest_key(cont):
    """ Key chest """
    own = cont.owner
    if (own['active'] == False):
        chest = small_chest(own, logic.OBJECT_CONSTANT.DUNGEON_KEY, "chest.dungeon.0.key.0")
        # Add appearance effect
        scene.addObject("effect.appearance_spark", chest, 200)
        # end
        own['active'] = True
        own['timer'] = 0.0
        #own.endObject()

def locked_door(cont):
    own = cont.owner
    door = scene.addObject("wood_door.locked", own)
    door['dungeon'] = 0
    own.endObject()

def active_interrupteur_0():
    logic.sendMessage("CHEST:APPEAR_CHEST_KEY.0")
    print("Activé")

def interrupteur(cont):
    own = cont.owner
    flag = scene.addObject("rock_flag", own)
    # Active interrupteur
    for obj in flag.children:
        if ("interrupteur" in obj.name):
            obj["activeFunction"] = active_interrupteur_0
