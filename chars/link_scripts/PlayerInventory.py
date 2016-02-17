# Imports
from bge import logic

class PlayerInventory:
	# Constants
	HEART = 0
	RUPEE = 1
	SWORD = 2
	KEY = 3

	def __init__(self, player):
		"""
		We have many type of object in iventory:
			- Equipement
			- Map and Bousol
			- Heart Container
			- Rupee Purse
			- Bomb Purse
		"""
		self.player = player;
		# * Init or not Inventory
		if not 'Inventory' in logic.globalDict['Player'] :
			# * ITEMS
			items_obj = {'bow' : {'have' : False, 'equiped' : False},
				'boomrang' : {'have' : False, 'equiped' : False},
				'bomb' : {'have' : False, 'equiped' : False},
				'bomb_arrow' : {'have' : False, 'equiped' : False},
				'hookshot' : {'have' : False, 'equiped' : False},
				'glass' : {'have' : False, 'equiped' : False},
				'flipper' : {'have' : False, 'equiped' : False},
				'shovel' : {'have' : False, 'equiped' : False},
				'roc_plume' : {'have' : False, 'equiped' : False}
			}

			items = {
				'Objects' : items_obj
			}
			# * EQUIPEMENTS
			swordEquip = {'basic_sword' : {'have' : True, 'equiped' : True},
				'mystic_sword' : {'have' : False, 'equiped' : False},
				'hero_sword' : {'have' : False, 'equiped' : False}}

			shieldEquip = {'wood_shield' : {'have' : False, 'equiped' : False},
				'hylian_shield' : {'have' : False, 'equiped' : False},
				'fairy_shield' : {'have' : False, 'equiped' : False}}

			equipement = {'Swords' : swordEquip,
				'Shields' : shieldEquip }

			# * DUNGEONS KEYS
			dungeon_inventory = {
				'Keys' : {'quantity' : 0},
				'Boss_Key' : {'have' : False},
				'Map' : {'have' : False},
				'Compass' : {'have' : False}
			}

			logic.globalDict['Player']['Inventory'] = {}
			logic.globalDict['Player']['Inventory']['Object'] =  {}
			# Dungeon inventory
			logic.globalDict['Player']['Inventory']['Dungeon'] = [{}]
			logic.globalDict['Player']['Inventory']['Dungeon'][0] = dungeon_inventory
			# Other
			logic.globalDict['Player']['Inventory']['Items'] = items
			logic.globalDict['Player']['Inventory']['Equipement'] = equipement

	def getSession(self, id_equip):
		session = ""
		if "sword" in id_equip:
			session = "Swords"
		elif "shield" in id_equip:
			session = "Shields"
		return session

	def getEquipement(self):
		return logic.globalDict['Player']['Inventory']['Equipement']

	def getEquipementSession(self, session):
		return logic.globalDict['Player']['Inventory']['Equipement'][session]

	def getDungeonKeyQuantity(self, dungeon):
		return logic.globalDict['Player']['Inventory']['Dungeon'][dungeon]['Keys']['quantity']

	def haveEquipement(self, id_equip):
		return self.getEquipement()[self.getSession(id_equip)][id_equip]['have']

	def equipAnyEquipementSession(self, session):
		for equip in self.getEquipement()[session].values():
			if equip['equiped'] == True:
				return True
		return False

	def equipementIsEquiped(self, id_equip):
		return self.getEquipement()[self.getSession(id_equip)][id_equip]['equiped']

	def equipEquipement(self, session, id_equip):
		current_item = logic.globalDict['Player']['Inventory']['Equipement'][session][id_equip]
		# If the current item isn't already equiped
		if (current_item['have'] and current_item['equiped'] == False):
			# First de-equip
			for item in logic.globalDict['Player']['Inventory']['Equipement'][session].values():
				item['equiped'] = False
			current_item['equiped'] = True
			# Ok !
			return True
		else:
			return False

	def addEquipement(self, id_equip):
		if "sword" in id_equip:
			session = "Swords"
		elif "shield" in id_equip:
			session = "Shields"
		self.getEquipement()[session][id_equip]['have'] = True

	def addKey(self, dungeon):
		logic.globalDict['Player']['Inventory']['Dungeon'][dungeon]['Keys']['quantity'] += 1
		logic.playerHUD.updateDungeonKey()

	def addObject(self, objData):
		objectInventory = logic.globalDict['Player']['Inventory']['Object']
		type = objData['type']

		# Rupee
		if (type == 1):
			self.player.rupeeContainer.gainRupee(objData['value'])
		elif (type == 2):
			self.addEquipement(objData['value'])
		elif (type == 3):
			self.addKey(objData['value'])

	# User
	def useDungeonKey(self, dungeon):
		if ( self.getDungeonKeyQuantity(dungeon) > 0):
			logic.globalDict['Player']['Inventory']['Dungeon'][0]['Keys']['quantity'] -= 1
			logic.playerHUD.updateDungeonKey()
			return True
		else:
			return False
