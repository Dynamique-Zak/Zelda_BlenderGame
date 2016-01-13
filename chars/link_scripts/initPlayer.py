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

from .AxisOrientation import AxisOrientation

from .PlayerRig import PlayerRig
from .PlayerPhysic import PlayerPhysic
from .PlayerClass import Player
from .PlayerConstants import PlayerState

scene = logic.getCurrentScene()

def initPlayer(cont):
	#logic.globalDict['SunPos'] = scene.objects['Sun'].worldPosition
	#
	logic.globalDict['Player'] = {}

	own = cont.sensors['player'].owner
	rig = cont.sensors['arm_sensors'].owner
	backCam = cont.sensors['backCam_sensors'].owner
	orientController = scene.objects['orientController']

	groundSens = cont.sensors['groundSens']

	track_orient = cont.actuators['track_orient']

	# instance physic
	physic = PlayerPhysic(groundSens)

	# instance rig
	rig = PlayerRig(rig)

	# instance axis orient
	orientController = AxisOrientation(orientController)

	# instance player
	own = Player(own, rig, physic, track_orient, backCam)

	# load data
	own.loadData()

	# Add hud scene
	logic.addScene("HUD")

	# start with fall state
	own.switchState(PlayerState.FALL_STATE)

	logic.globalDict['player'] = own

def step2(cont):
	own = cont.sensors['player'].owner
	logic.globalDict['player'] = own
	# * LOAD HUD SCENE
	scenes = logic.getSceneList()

	for i in scenes:
		print(i.name)
		if i.name == "HUD":
			hudScene = i

	hudScene.objects['HUD']['initHUD'] = True
	# hud transition
	#hudScene.setHeart(logic.globalDict['heart'], logic.globalDict['maxHeart'])
	#logic.playerHUD.fadeOutToHiddenTransition()

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

	# step 3 play
	if (logic.globalDict['stepInit'] == 4):
		logic.globalDict['stepInit'] = 0
		logic.globalDict['initPlayer'] = True
		cont.activate('main_state')

def init(cont):
	if not 'stepInit' in logic.globalDict:
		logic.globalDict['stepInit'] = 0
	firstInit(cont)
