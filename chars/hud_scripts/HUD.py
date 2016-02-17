from bge import logic, types, events
import bge
from hud_scripts.MessageBox import MessageBox
from hud_scripts.Inventory import Inventory

import aud
import os
import bpy

# load message box sounds
device = aud.device()
# load sound file (it can be a video file with audio)
sfxPath = bpy.path.abspath("//../audio/hud_song/")
signal_parry = aud.Factory(sfxPath + "signal_parry.wav")


#
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
objects = scene.objects

heartContainer = logic.globalDict['Player']['heartContainer'];
rupeeContainer = logic.globalDict['Player']['rupeeContainer'];

class PlayerHUD(types.KX_GameObject):
	def __init__(self, own, msgBox):
		self.messageBox = msgBox
		self.lowHealth = False
		low_health = aud.Factory(sfxPath + "low_health.wav")
		self.handleLowHealth = None
		self.low_healthLoop = low_health.loop(-1)

	def setFadeOutTransition(self, state):
		obj = objects['transition.fadeOut']
		if (state):
			obj['toHide'] = True
			obj['toDisplay'] = False
		else:
			obj['toDisplay'] = True
			obj['toHide'] = False

	def changeActionText(self, text):
		objects['actionText']['Text'] = text

	def resetActionText(self):
		objects['actionText']['Text'] = ""

	def setForegroundTarget(self, state):
		objects['target_foreground']['active'] = state

	def setTargetHUDState(self,val):
		objects['targetCursor']['activate'] = val

	def setTargetCursorPosition(self, pos):
		x = -4.5 + ( pos[0] * 9 )
		y = 3.5 - ( pos[1] * 7 )
		objects['targetCursor'].worldPosition = [x, y, 1]

	def setActionReactionButtonVisible(self, state=True):
		objects['action_reaction_icon.border'].setVisible(state)
		objects['action_reaction_icon.a'].setVisible(state)
		if (state == True):
			device.play(signal_parry)

	def setMiniMap(self, name):
		mini_map = objects['mini_map']
		imagePath = logic.expandPath('//../textures/hud/maps/' + name)
		matID = bge.texture.materialID(mini_map, "MAminiMap")
		# get the texture
		tex = bge.texture.Texture(mini_map, matID)
		logic.texture = tex
		# get image used as the texture source
		logic.texture.source = bge.texture.ImageFFmpeg(imagePath)
		# display the image
		logic.texture.refresh(False)
		# Display plane
		mini_map.setVisible(True)

	def displayInventory(self):
		objects['Inventory'].display()

	def closeInventory(self):
		objects['Inventory'].close()

	def updateDungeonKey(self):
		indicator = objects['dungeon.key.text']
		indicator['Text'] = logic.globalDict['Player']['Inventory']['Dungeon'][logic.currentDungeon]['Keys']['quantity']

	def updateRupee(self):
		rubi_text = objects['rubis_text']
		rubi_text['Text'] = rupeeContainer['rupee']

	#==================================================================================
	# * GESTION DES COEURS
	#==================================================================================
	def updateHeart(self):
		# Recupere les variables globales
		maxcoeurs = heartContainer['maxHeart']
		vie = heartContainer['heart']

		dx=0
		dy=0
		coeur=[0]*20

		for i in range(0,20):

			diff=(vie-int(vie))

			if i<10:
				coeur[i]=scene.objects["c.00"+str(i)]
			else:
				coeur[i]=scene.objects["c.0"+str(i)]

			if i>=maxcoeurs:#cache les coeurs inexistants
				coeur[i].setVisible(0)

			#Vie pleine:
			elif maxcoeurs==vie:
				if i==(maxcoeurs-1):
					dx=0.5
					dy=-0.5
					coeur[i]["ipo"]=1

			elif 0<=diff<0.25 and (i)==int(vie-1):
					dx=0.5
					dy=-0.5
					coeur[i]["ipo"]=1

			elif i==int(vie):


			#coeur vide
				if 0<=diff<0.25 :
					dx=0
					dy=-0.5
					coeur[i]["ipo"]=0
			#1/4 de coeur
				if 0.25<=diff<0.5:
					dx=0
					dy=-0.25
					coeur[i]["ipo"]=1
			#1/2 coeur
				if 0.5<=diff<0.75:
					dx=0.5
					dy=-0.25
					coeur[i]["ipo"]=1
			#3/4 de coeur
				if 0.75<=diff<1:
					dx=0.5
					dy=0
					coeur[i]["ipo"]=1

			#coeurs vide si au dessus
			elif i>int(vie) or(i==0 and vie==0):
				dx=0
				dy=-0.5
				coeur[i]["ipo"]=0

			#coeurs plein si en dessous de la limite
			elif i<int(vie) and vie>0:
				dx=0
				dy=0
				coeur[i]["ipo"]=0

			#OUTIL DES MOUVEMENT UV
			for mesh in coeur[i].meshes:
				#1
				vert= mesh.getVertex(0, 0)
				UV=vert.getUV()
				vert.setUV([0+dx,1+dy])
				#v2
				vert=mesh.getVertex(0,3)
				UV=vert.getUV()
				vert.setUV([0.5+dx,1+dy])
				#v3
				vert=mesh.getVertex(0,2)
				UV=vert.getUV()
				vert.setUV([0.5+dx,0.75+dy])
				#v4
				vert=mesh.getVertex(0,1)
				UV=vert.getUV()
				vert.setUV([0+dx,0.75+dy])

	def updateMiniMap(self):
		cursor = scene.objects['mini_map_player_cursor']
		mini_map_cont_pos = scene.objects['mini_map_cont'].worldPosition
		cursor.orientation = logic.player.orientation
		x = mini_map_cont_pos[0] + ( logic.player.worldPosition[0] / 45 )
		y = mini_map_cont_pos[1] + ( logic.player.worldPosition[1] / 45 )
		cursor.worldPosition[0] = x
		cursor.worldPosition[1] = y

	def low_healt(self, isLow):
		if (isLow):
			if (self.lowHealth == False):
				self.lowHealth = isLow
				self.handleLowHealth = device.play(self.low_healthLoop)
		else:
			if (self.handleLowHealth != None and self.lowHealth):
				self.lowHealth = isLow
				self.handleLowHealth.stop()

	def main(self):
		# update msg box
		self.messageBox.main()
		logic.hudInventory.main()

#==================================================================================
# * Main
#==================================================================================
def init(cont):
	own = cont.owner
	# init
	if not 'init' in own:
		msgBox = MessageBox(scene.objects['MessageBox'])
		own = PlayerHUD(own, msgBox)
		# Init inventory
		# Inventory
		logic.hudInventory = Inventory(scene.objects['Inventory'])
		# Update
		own.updateRupee()
		own.updateHeart()
		own.updateDungeonKey()

		if ('miniMap' in logic.globalDict):
			name = logic.globalDict['miniMap']
			own.setMiniMap(name)
		# logic
		logic.playerHUD = own
		own['init'] = True
	else:
		own.main()
		logic.playerHUD = own
