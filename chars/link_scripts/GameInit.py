from bge import logic

# TYPE
RUPEE = 1
EQUIPEMENT = 2
KEY = 3

class ObjectConstant:
	RUPEE = 0
	BASIC_SWORD = 1
	MYSTIC_SWORD = 2
	HERO_SWORD = 3
	WOOD_SHIELD = 4
	DUNGEON_KEY = 5

def addObject(name, id_obj, description, gain_description, type_obj, value):
	logic.globalDict['Objects'].append({'name' : name, 'id_obj' : id_obj, 'description' : description,
	'description2': gain_description, 'type' : type_obj, 'value' : value})

def initGame():
	# Init constant
	logic.OBJECT_CONSTANT = ObjectConstant()

	# Init dungeon
	logic.currentDungeon = 0

	if not 'Objects' in logic.globalDict:
		# Init logic globalDict Object
		logic.globalDict['Objects'] = []

		# Set default obj
		addObject('Rubis vert', 'green_rupee', 'Un rubis vert vaut 1 rubi.', 'Fantastique 1 rubi..... Il y\'a beaucoup mieux c\'est sur...', 1, 1)
		addObject('Epee debutant', 'basic_sword', 'L\'Epee du debutant !', 'Vous avez obtenu de quoi agress... vous defendre !', EQUIPEMENT, 'basic_sword')
		addObject('Epee  mystique', 'basic_sword', 'L\'Epee des fees !', 'Vous avez obtenu l\'epee mystique des fee !', EQUIPEMENT, 'mystic_sword')
		addObject('Epee  du hero', 'basic_sword', 'L\'Epee des fees !', 'Vous avez obtenu l\'epee mystique des fee !', EQUIPEMENT, 'hero_sword')
		addObject('Bouclier en bois', 'wood_shield', 'Bouclier en bois d\'une ancienne civilisation', 'Vous avez obtenu un bouclier en bois !', EQUIPEMENT, 'wood_shield')
		addObject('Cle du donjon', 'dungeon_key', 'Un clé de donjon', 'Vous avez obtenu une cle du donjon !', KEY, 0)

		# Global dict for
		logic.globalDict['Chests'] = {'chest.basic_sword' : False}

	# Finally send init message
	logic.sendMessage("INIT_LEVEL")
