from bge import logic
import mathutils

scene = logic.getCurrentScene()

class PlayerZTargeting:

	def __init__(self):
		self.targetObject = None
		self.detectedObject = None
		self.active = False

	def canTargetObject(self):
		player = scene.objects['Link']
		if ( player.gamepad.isZPressed() and self.detectedObject != None ):
			self.activeTargetMode()
			return True
		else:
			return False

	def activeTargetMode(self):
		self.targetObject = self.detectedObject
		self.setupTargetObject()
		logic.playerHUD.setTargetHUDState(True)
		self.active = True

	def deactivateTargetMode(self):
		# get objects
		player = scene.objects['Link']
		camera = scene.objects['MainCam']
		headTracker = scene.objects['headTracker']

		# setup property
		camera['tracked_player'] = True
		camera['lookObject'] = False
		player.rig['armConstraint'] = False

		self.targetObject = None
		logic.playerHUD.setTargetHUDState(False)
		self.active = False

	def activeHeadTrack(self):
		# get objects
		player = scene.objects['Link']
		player.rig['armConstraint'] = True

	def deactiveHeadTrack(self):
		# get objects
		player = scene.objects['Link']
		player.rig['armConstraint'] = False

	def canFindObject(self):
		cont = logic.getCurrentController()
		collision = cont.sensors['targetCollision']
		# if detect
		if collision.positive:
			return True
		else:
			return False

	def findObject(self):
		cont = logic.getCurrentController()
		collision = cont.sensors['targetCollision']
		# if detect
		if collision.positive:
			self.detectedObject = collision.hitObject # After list object
			logic.playerHUD.setTargetHUDState(True)
			self.updateTargetCursor(self.detectedObject)
		else:
			logic.playerHUD.setTargetHUDState(False)
			self.detectedObject = None

	def targetMovement(self, player):
		# if joy connected
		moved = False
		maxSpeed = 5.0
		axis = player.gamepad.getJoyAxis1()
		x_axis = axis[0]
		y_axis = axis[1]

		x_force = 0.0
		y_force = 0.0

		# apply
		if (y_axis != 0.0):
			y_force = maxSpeed * -y_axis
		if (x_axis != 0.0):
			x_force = maxSpeed * x_axis

		# apply movement
		player.linearVelocity[0] = x_force
		player.linearVelocity[1] = y_force

		# tes
		if ( y_force != 0.0 or x_force != 0.0):
			moved = True
		# return statement
		return moved

	def updateTargetCursor(self, obj):
		camera = scene.objects['MainCam']
		# Apply target cursor
		logic.playerHUD.setTargetCursorPosition(camera.getScreenPosition(obj))

	def updateObjectsTransformation(self, player, headTracker, midPoint, camera):
		#  Apply headTracker and midPoint position
		headTracker.worldPosition = self.targetObject.worldPosition
		midPoint.worldPosition = (player.worldPosition + self.targetObject.worldPosition) / 2.0

		# variables for calculate new cam pos
		midPointPos = midPoint.worldPosition
		targetPos = self.targetObject.worldPosition

		z_dist = midPointPos[2] - targetPos[2]
		z_cam = midPointPos[2] - z_dist
		pos = mathutils.Vector([-2, -5 - abs(z_cam), 0])
		pos.rotate(player.orientation)

		# Update cursor pos
		self.updateTargetCursor(self.targetObject)

		# Apply camera position
		camera.worldPosition = player.worldPosition
		camera.worldPosition[2] = z_cam + 1
		camera.worldPosition += pos

	def setupTargetObject(self):
		# get objects
		player = scene.objects['Link']
		camera = scene.objects['MainCam']
		midPoint = scene.objects['midPointTarget']
		headTracker = scene.objects['headTracker']

		# setup property
		camera['tracked_player'] = False
		camera['lookObject'] = True
		player.rig['armConstraint'] = True

		# apply transform
		self.updateObjectsTransformation(player, headTracker, midPoint, camera)


	def trackTargetObject(self, cont):
		# player track the targetObject
		trackAct = cont.actuators['track_orient']
		trackAct.object = self.targetObject
		cont.activate(trackAct)

		# update mid poind target positif
		player = scene.objects['Link']
		camera = scene.objects['MainCam']
		midPoint = scene.objects['midPointTarget']
		headTracker = scene.objects['headTracker']

		# actuators
		trackAct = cont.actuators['track_orient']
		trackAct.object = self.targetObject
		cont.activate('track_orient')

		# apply transform
		self.updateObjectsTransformation(player, headTracker, midPoint, camera)
