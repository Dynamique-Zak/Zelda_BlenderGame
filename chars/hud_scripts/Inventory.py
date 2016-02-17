from bge import logic, types
import bpy
import aud

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
hud_sfx = bpy.path.abspath("//../audio/hud_song/")
cursorMoveSound = aud.Factory( hud_sfx + "pm_cursor_move.wav" )

# scene objects
scene = logic.getCurrentScene()
objects = scene.objects

# objects
cursor = objects['cursorItem']

# Gamepad
gamepad = logic.globalDict['Player']['Gamepad']

#Constansts
nbr_line = 3
nbr_column = 3
nbr_items = 9
JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED

class Inventory(types.KX_GameObject):
	# AUDIO Constants
	CURSOR_MOVE_AUDIO = 0
	CURSOR_SELECT_AUDIO = 1
	ERROR_AUDIO = 2
	# SESSION Constants
	ITEMS_SESSION = 0
	EQUIP_SESSION = 1

	# Sub Session
	SESSION_STR = [
		[ ['items.objects'], 'Objects' ],
		[ ['equip.swords', 'Swords'], ['equip.shields', 'Shields'] ]
	]

	EQUIP_SESSION_STR = [ ['equip.swords', 'Swords'], ['equip.shields', 'Shields'] ]

	def __init__(self, own):

		self.indexItem = 0
		self.rows = 0
		self.columns = 0
		self.active = False
		self.session = -1
		self.subSession = -1
		self.audio = [None, aud.Factory( hud_sfx + "pm_cursor_select.wav" ), aud.Factory( hud_sfx + "error.wav" )]

		# Arrays
		self.sessionSpace = [
			[9, 3],
			[3, 3]
		]

		self.arrayItem = [
			[ ['bow', 'boomrang', 'bomb', 'bomb_arrow', 'hookshot', 'glass', 'flipper', 'shovel', 'roc_plume'] ],
			[ ['basic_sword', 'mystic_sword', 'hero_sword'], ['wood_shield', 'hylian_shield', 'fairy_shield']]
		]

		items_list = logic.globalDict['Player']['Inventory']['Items']['Objects']
		equip_list = logic.globalDict['Player']['Inventory']['Equipement']

		self.sessionData = [
			[self.initArrayEquipement(Inventory.ITEMS_SESSION, 0, items_list)],
			[self.initArrayEquipement(Inventory.EQUIP_SESSION, 0, equip_list['Swords']), self.initArrayEquipement(Inventory.EQUIP_SESSION, 1, equip_list['Shields'])]
		]

	def initArrayEquipement(self, session, subSession, lists):
		array = []
		for key in self.arrayItem[session][subSession]:
			item = lists[key]
			array.append("Inventory." + Inventory.SESSION_STR[session][subSession][0] + "." + key)
		# for item in lists.values():
		# 	print(item['id'])
		# 	array.append("Inventory." + session + "." + item['id'])
		return array

	def playAudio(self, index):
		device.play(self.audio[index])

	def display(self):
		self.active = True
		self.setVisible(True, True)
		# Display from swords session
		self.displayHavedObject(logic.globalDict['Player']['Inventory']['Equipement']['Swords'], Inventory.EQUIP_SESSION, 0)
		# Display from shields session
		self.displayHavedObject(logic.globalDict['Player']['Inventory']['Equipement']['Shields'], Inventory.EQUIP_SESSION, 1)
		# Hide inventory
		objects['Inventory.items'].setVisible(False, True)
		# Init default session
		self.setInventorySession(Inventory.EQUIP_SESSION, 0)

	def displayHavedObject(self, lists, session, subSession):
		# Display haved object
		have = False
		for key in self.arrayItem[session][subSession]:
			item = lists[key]
			obj = objects['Inventory.' + Inventory.SESSION_STR[session][subSession][0] + '.' + key]

			if (item['equiped']):
				self.setSelectCursor(Inventory.EQUIP_SESSION_STR[subSession][0], obj)
				have = True

			obj.setVisible(item['have'])
		if not have :
			self.setSelectCursor(Inventory.EQUIP_SESSION_STR[subSession][0], None)

	def setInventorySession(self, session, subSession):
		if (self.session != session):
			self.session = session
			# Define rows and cols from session
			if (session == Inventory.EQUIP_SESSION):
				self.rows = 2
				self.columns = 3
				self.nbr_items = 6
			# ...
			self.subSession = subSession
			# Init cursor pos to first obj session
			self.updateCursor()

	def setSelectCursor(self, session, reference):
		cursor = objects['Inventory.' + session + '.selected_cursor']
		if reference != None:
			if (type(reference) is str):
				reference = objects[reference]
			cursor.worldPosition = reference.worldPosition
			if (not cursor.visible):
				cursor.setVisible(True)
		else:
			cursor.setVisible(False)

	def close(self):
		self.active = False
		self.setVisible(False, True)

	def activeObject(self, id):
		logic.globalDict['Player']['Inventory'][id][2] = True

	def updateCursor(self):
		inventory = logic.globalDict['Player']['Inventory']
		reference = self.sessionData[self.session][self.subSession][self.indexItem]
		itemObj = objects[reference]
		cursor.worldPosition[0] = itemObj.worldPosition[0]
		cursor.worldPosition[1] = itemObj.worldPosition[1]

	def nextSession(self, nextVal):
		next_session = self.subSession + nextVal
		nbr_session = len(self.sessionData[self.session])
		if ( next_session >= nbr_session or next_session < 0):
			return False
		else:
			self.subSession = next_session
			# If back go to the last index of next session
			if (nextVal < 0):
				maxPlace = self.sessionSpace[self.session][self.subSession]
				self.indexItem = maxPlace-1
			else:
				self.indexItem = 0
			# Update cursor
			self.updateCursor()
			return True

	def nextItem(self, nextVal=1):
		nextIndex = self.indexItem + nextVal
		maxPlace = self.sessionSpace[self.session][self.subSession]
		if (nextIndex < self.nbr_items):
			# If change session
			if (nextIndex >= maxPlace or nextIndex < 0):
				# If can change session
				if (self.nextSession(nextVal)):
					device.play(cursorMoveSound)
			else:
				self.indexItem = nextIndex
				self.updateCursor()
				device.play(cursorMoveSound)
			# self.arrayItem[self.indexItem]
			# self.updateCursor()
			# reference = self.sessionData[self.session][self.subSession][self.indexItem]
			# self.setCursor(reference)
			# play audio sound
		else:
			pass
			# block

	def applyObject(self):
		# xButton = objects['XButton']
		# name = "boomrang_iconeItem"
		# if (len(xButton.children) == 0 or xButton.children[0].name != name):
		# 	print('lol')
		# 	xButtonObject = scene.addObject("boomrang_iconeItem", xButton, 0)
		# 	xButtonObject.setParent(xButton)
		if (self.session == Inventory.EQUIP_SESSION):
			# If can equip
			idObj = self.arrayItem[self.session][self.subSession][self.indexItem]
			if ( logic.player.inventory.equipEquipement(Inventory.EQUIP_SESSION_STR[self.subSession][1], idObj) ):
				reference = self.sessionData[self.session][self.subSession][self.indexItem]
				self.setSelectCursor(Inventory.EQUIP_SESSION_STR[self.subSession][0], reference)
				# Update player
				logic.player.fightManager.updateEquipement()
				# Play audio
				self.playAudio(Inventory.CURSOR_SELECT_AUDIO)
			else:
				# Play error audio
				self.playAudio(Inventory.ERROR_AUDIO)

	def main(self):
		# if is activate
		if (self.active):
			# control the cursor
			if ( gamepad.isRightPressed(JUST_ACTIVATED) ):
				self.nextItem()
			elif ( gamepad.isLeftPressed(JUST_ACTIVATED) ):
				self.nextItem(-1)
			elif ( gamepad.isDownPressed(JUST_ACTIVATED) ):
				self.nextItem(self.columns)
			elif ( gamepad.isUpPressed(JUST_ACTIVATED) ):
				self.nextItem(-self.columns)
			# activate current object to a case
			elif ( gamepad.isItemXPressed(JUST_ACTIVATED) ):
				self.applyObject()
			# Activate with a
			elif ( gamepad.isActionPressed(JUST_ACTIVATED)):
				self.applyObject()
			# If close it
			elif ( gamepad.isZPressed(JUST_ACTIVATED) ):
				self.close()
				logic.player.scene.resume()
