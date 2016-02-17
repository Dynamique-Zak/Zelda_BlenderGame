from bge import logic
import sys

#sys.path.append('../../scripts')
#sys.path.append('../scripts/player/')

#dir = os.path.abspath(__file__ + "../../../../")
#filename = os.path.join(dir, 'scripts/')
#filenamePlayer = os.path.join(dir, 'scripts/player/')

#loader = importlib.machinery.SourceFileLoader('AxisOrientation.*', filename + 'AxisOrientation.py')
#AxisOrientation = loader.load_module().AxisOrientation

#loader = importlib.machinery.SourceFileLoader('PlayerRig.*', filenamePlayer + 'PlayerRig.py')
#PlayerRig = loader.load_module().PlayerRig

#loader = importlib.machinery.SourceFileLoader('PlayerPhysic.*', filenamePlayer + 'PlayerPhysic.py')
#PlayerPhysic = loader.load_module().PlayerPhysic

#loader = importlib.machinery.SourceFileLoader('PlayerClass.*', filenamePlayer + 'PlayerClass.py')
#PlayerClass = loader.load_module()
import os
import sys

from .AxisOrientation import AxisOrientation

from link_scripts.GameInit import initGame

from link_scripts.PlayerRig import PlayerRig
from link_scripts.PlayerPhysic import PlayerPhysic
from link_scripts.PlayerClass import Player
from link_scripts.PlayerConstants import PlayerState

scene = logic.getCurrentScene()

def loadConfFile():
	if ( not 'CONFIGURATION' in logic.globalDict ):
		# Create empty configuration
		logic.globalDict['CONFIGURATION'] = {}

		filename = os.path.dirname( __file__ ) + "/../../conf.txt"
		print(filename)
		# Read file content for future modification
		with open(filename, "r") as myFile:
			lines = myFile.readlines()

			# Search State part and Constant name
			for line in lines:
				token = line.split("=")

				if (token[0] == "joystick"):
					logic.globalDict['CONFIGURATION']['useJoystick'] = int(token[1])

				if (token[0] == "active_auto_cam"):
					logic.globalDict['CONFIGURATION']['active_auto_cam'] = int(token[1])

def initPlayer(cont):
	print("Player initialization")
	loadConfFile()
	# Init game
	logic.camObstaclePosition = None

	initGame()

	#logic.globalDict['SunPos'] = scene.objects['Sun'].worldPosition
	#
	if not 'Player' in logic.globalDict:
		logic.globalDict['Player'] = {}

	own = cont.sensors['player'].owner
	rig = cont.sensors['arm_sensors'].owner
	backCam = cont.sensors['backCam_sensors'].owner
	orientController = scene.objects['orientController']

	track_orient = cont.actuators['track_orient']

	# Active camera
	if logic.globalDict['CONFIGURATION']['active_auto_cam'] == 1:
		print("OK")
		scene.active_camera = backCam

	# instance physic
	physic = PlayerPhysic()

	# instance rig
	rig = PlayerRig(rig)

	# instance axis orient
	orientController = AxisOrientation(orientController)

	# Instance player
	own = Player(own, rig, physic, track_orient, backCam)

	# Load data
	own.loadData()

	# Init equipement visibility
	own.fightManager.initEquipement()

	# Start pos from level
	if ('level' in logic.globalDict):
		if ('startPos' in logic.globalDict['level']):
			own.worldPosition = logic.globalDict['level']['startPos']
			a = logic.globalDict['level']['targetVec']
			vec = [a[0], a[1], a[2]]
			own.alignAxisToVect(vec, 0, 1)
	else:
		logic.globalDict['level'] = {}
		vec = [1, 0, 0]
		own.alignAxisToVect(vec, 0, 1)

	# Add hud scene
	logic.addScene("HUD")

	# start with fall state
	own.switchState(PlayerState.FALL_STATE)

	logic.player = own
	logic.globalDict['player'] = own

def step2(cont):
	own = cont.sensors['player'].owner
	logic.globalDict['player'] = own
	# * LOAD HUD SCENE
	scenes = logic.getSceneList()

	for i in scenes:
		if i.name == "HUD":
			hudScene = i

	if 'levelInit' in scene.objects:
		logic.globalDict['miniMap'] = scene.objects['levelInit']['miniMap']
	hudScene.objects['HUD']['initHUD'] = True
	# hud transition
	#hudScene.setHeart(logic.globalDict['heart'], logic.globalDict['maxHeart'])
	#hudScene.objects['HUD'].fadeOutToHiddenTransition()

def loadPlayer(cont):
	own = cont.sensors['player'].owner
	# load player
	own = logic.globalDict['player']
	# step 2 hud
	step2(cont)
	# go to main
	cont.activate('main_state')

def firstInit(cont):
	logic.globalDict['stepInit'] += 1

	# step one init player and other
	if (logic.globalDict['stepInit'] == 2):
		initPlayer(cont)
	# step 2 detect begin
	if (logic.globalDict['stepInit'] == 3):
		step2(cont)

	if (logic.globalDict['stepInit'] == 5):
		# active fadeout for display
		logic.playerHUD.setFadeOutTransition(True)

	# step 3 play
	if (logic.globalDict['stepInit'] == 6):
		logic.globalDict['stepInit'] = 0
		logic.globalDict['initPlayer'] = True
		cont.activate('main_state')

def init(cont):
	if not 'stepInit' in logic.globalDict:
		logic.globalDict['stepInit'] = 0
	firstInit(cont)
