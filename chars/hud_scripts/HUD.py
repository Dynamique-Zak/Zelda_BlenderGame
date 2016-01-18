from bge import logic, types, events
from hud_scripts.MessageBox import MessageBox

#
scene = logic.getCurrentScene()
cont = logic.getCurrentController()
objects = scene.objects

heartContainer = logic.globalDict['Player']['heartContainer'];
rupeeContainer = logic.globalDict['Player']['rupeeContainer'];

class PlayerHUD(types.KX_GameObject):
	def __init__(self, own, msgBox):
		self.messageBox = msgBox

	def fadeOutToHiddenTransition(self):
		objects['plan_fadeOut']['toHide'] = True
		objects['plan_fadeOut']['toDisplay'] = False

	def fadeOutToDisplayTransition(self):
		objects['plan_fadeOut']['toDisplay'] = True
		objects['plan_fadeOut']['toHide'] = False

	def changeActionText(self, text):
		objects['actionText']['Text'] = text

	def resetActionText(self):
		objects['actionText']['Text'] = ""

	def setTargetHUDState(self,val):
		objects['targetCursor']['activate'] = val

	def setTargetCursorPosition(self, pos):
		x = -4.5 + ( pos[0] * 9 )
		y = 3.5 - ( pos[1] * 7 )
		objects['targetCursor'].worldPosition = [x, y, 1]

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
					dx=0.25
					dy=-0.5
					coeur[i]["ipo"]=1

			elif 0<=diff<0.25 and (i)==int(vie-1):
					dx=0.25
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
					dx=0.25
					dy=-0.25
					coeur[i]["ipo"]=1
			#3/4 de coeur
				if 0.75<=diff<1:
					dx=0.25
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
				vert.setUV([0.25+dx,1+dy])
				#v3
				vert=mesh.getVertex(0,2)
				UV=vert.getUV()
				vert.setUV([0.25+dx,0.75+dy])
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

	def low_healt(self, cont):
		heartContainer = logic.globalDict['Player']['heartContainer']
		maxcoeurs = heartContainer['maxHeart']
		vie = heartContainer['heart']
		moyenne = (vie / maxcoeurs) * 100
		if (moyenne < 30.0) :
			#activate low ghealt
			cont.activate('low_healt')
		else :
			cont.deactivate('low_healt')

	def main(self):
		# update msg box
		self.messageBox.main()

#==================================================================================
# * Main
#==================================================================================
def init(cont):
	own = cont.owner
	# init
	if not 'init' in own:
		msgBox = MessageBox(scene.objects['MessageBox'])
		own = PlayerHUD(own, msgBox)
		# Update
		own.updateRupee()
		own.updateHeart()
		# logic
		logic.playerHUD = own
		own['init'] = True
	else:
		own.main()
		logic.playerHUD = own
