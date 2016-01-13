from bge import logic, types
import bpy
import aud

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
cursorMoveSound = aud.Factory( bpy.path.abspath("//../audio/hud_song/dialogue_next.wav") )

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

	def __init__(self, own):
		self.indexItem = 0
		self.active = True
		self.arrayItem = ['arc', 'boomrang', 'canne_peche', 'fleche_bombe', 'grappin', 'loupe', 'palmes', 'pelle', 'plume_roc']

		# Si l'inventaire n'a pas déja été initialisé
		if (not 'Inventory' in logic.globalDict['Player']):
			# init object
			arc =  ['Arc', '', False]
			boomrang = ['Boomrang', '', False]
			canne_peche = ['Canne a peche', '', False]
			fleche_bombe = ['Fleche de bombe', '', False]
			grappin = ['Grappin', '', False]
			loupe = ['Loupe', '', False]
			palmes = ['Palmes', '', False]
			pelle = ['Pelle', '', False]
			plume_roc = ['Plume de roc', '', False]

			logic.globalDict['Player']['Inventory'] = {'arc' : arc, 'boomrang' : boomrang, 'canne_peche' : canne_peche,
			'fleche_bombe' : fleche_bombe, 'grappin' : grappin, 'loupe' : loupe, 'palmes' : palmes, 'pelle' : pelle, 'plume_roc' : plume_roc}

	def activeObject(self, id):
		logic.globalDict['Player']['Inventory'][id][2] = True

	def updateCursor(self):
		inventory = logic.globalDict['Player']['Inventory']
		idItem = self.arrayItem[self.indexItem]
		itemObj = objects[idItem + '_icone']
		cursor.worldPosition[0] = itemObj.worldPosition[0]
		cursor.worldPosition[1] = itemObj.worldPosition[1]

	def nextItem(self, nextVal=1):
		nextIndex = self.indexItem + nextVal
		if (nextIndex < nbr_items and nextIndex > -1):
			self.indexItem = nextIndex
			self.arrayItem[self.indexItem]
			self.updateCursor()
			# play audio sound
			device.play(cursorMoveSound)
		else:
			pass
			# block

	def applyObject(self):
		xButton = objects['XButton']
		name = "boomrang_iconeItem"
		if (len(xButton.children) == 0 or xButton.children[0].name != name):
			print('lol')
			xButtonObject = scene.addObject("boomrang_iconeItem", xButton, 0)
			xButtonObject.setParent(xButton)

	def main(self):
		# if is activate
		if (self.active):
			# control the cursor
			if ( gamepad.isRightPressed(JUST_ACTIVATED) ):
				self.nextItem()
			elif ( gamepad.isLeftPressed(JUST_ACTIVATED) ):
				self.nextItem(-1)
			elif ( gamepad.isDownPressed(JUST_ACTIVATED) ):
				self.nextItem(3)
			elif ( gamepad.isUpPressed(JUST_ACTIVATED) ):
				self.nextItem(-3)
			# activate current object to a case
			elif ( gamepad.isItemXPressed(JUST_ACTIVATED) ):
				self.applyObject()
