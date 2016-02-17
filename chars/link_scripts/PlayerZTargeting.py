from bge import logic
import mathutils

scene = logic.getCurrentScene()

class PlayerZTargeting:

	def __init__(self):
		self.targetObject = None
		self.detectedObject = None
		self.active = False
		self.parryTime = 0.0
		self.parry = False

	def canTargetObject(self):
		canTarget = False
		player = scene.objects['Link']
		if ( player.gamepad.isZPressed()):
			if (not 'actif' in self.targetObject):
				canTarget = True
			elif (self.targetObject['actif'] == True):
				canTarget = True
		# If finally can target active the target mode
		if (canTarget):
			self.activeTargetMode()
		# return statement
		return canTarget

	def isHaveTargetObject(self):
		if (self.targetObject != None):
			return True
		else:
			return False

	def zTarget(self):
		player = scene.objects['Link']
		if (player.gamepad.isZPressed()):
			self.activeTargetMode()
			player.camManager.deactiveLookPlayer()
			return True
		else:
			return False

	def activeTargetMode(self):
		if (self.detectedObject != None):
			self.targetObject = self.detectedObject
			self.setupTargetObject()
			logic.playerHUD.setTargetHUDState(True)

		if (self.active != True):
			logic.playerHUD.setForegroundTarget(True)
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
		logic.playerHUD.setForegroundTarget(False)
		self.active = False
		cont = logic.getCurrentController()
		cont.deactivate('track_orient')

	def activeHeadTrack(self):
		"""
		Activate the head track
		"""
		# get objects
		player = scene.objects['Link']
		player.rig['armConstraint'] = True

	def deactiveHeadTrack(self):
		"""
		Deactivate the head track
		"""
		# get objects
		player = scene.objects['Link']
		player.rig['armConstraint'] = False

	def canParry(self):
		if (self.targetObject != None and self.targetObject.attackLevel > 0 and self.active):
			if (self.parry == False):
				self.parry = True
				logic.playerHUD.setActionReactionButtonVisible(True)

	def deactivateParry(self):
		if (self.parry):
			self.parry = False
			self.parryTime = 0.0
			logic.playerHUD.setActionReactionButtonVisible(False)

	def canFindObject(self):
		cont = logic.getCurrentController()
		collision = cont.sensors['targetCollision']
		# if detect
		if collision.positive:
			return True
		else:
			return False

	def findObject(self):
		"""
		Find a object in zone
		"""
		find = False
		cont = logic.getCurrentController()
		collision = cont.sensors['targetCollision']

		# if detect
		if collision.positive:
			# Get all objects detected
			listObject = collision.hitObjectList

			# Choose the appropriate enemy
			for obj in listObject:
				if ( ('actif' in obj and obj['actif']) and find == False):
					self.targetObject = obj
					find = True
		# If find object apply
		if (find):
			logic.playerHUD.setTargetHUDState(True)
			self.updateTargetCursor(self.targetObject)
		else:
			logic.playerHUD.setTargetHUDState(False)
			self.targetObject = None
		# Return statement
		return find

	def cancelTargetObject(self):
		"""
		Cancel all process for target a enemy
		"""
		# get objects
		cont = logic.getCurrentController()
		# Deactivate track to target object
		trackAct = cont.actuators['track_orient']
		trackAct.object = None
		cont.deactivate(trackAct)
		# Deactivate target
		logic.playerHUD.setTargetHUDState(False)
		# Deactivate head look
		self.deactiveHeadTrack()
		# Object None
		self.targetObject = None

	def canTargetCurrentObject(self):
		"""
		Test if can always target current enemy
		"""
		can = False
		if (self.targetObject['actif'] == True):
			can = True
		else:
			self.cancelTargetObject()
		return can

	def updateTargetMode(self):
		"""
		When target activate (Although no enemy has been detected), update that mode
		If not have have target object, find again when Z is hold
		"""
		player = scene.objects['Link']
		if (player.gamepad.isZPressed()):
			if (self.targetObject != None and self.canTargetCurrentObject()):
				cont = logic.getCurrentController()
				self.trackTargetObject(cont)
			else:
				player.camManager.cameraToBackPlayer()
				# Find enemy
				self.findObject()
				#self.deactivateTargetMode()
		else:
			self.deactivateTargetMode()

	def updateTargetCursor(self, obj):
		"""
		Update target cursor from HUD
		"""
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
		z_cam = midPointPos[2] + z_dist
		pos = mathutils.Vector([-2, -5 - abs(z_cam), 0])
		pos.rotate(player.orientation)

		# Update cursor pos
		self.updateTargetCursor(self.targetObject)

		# Apply camera position
		if (logic.camObstaclePosition == None):
			camera.worldPosition = player.worldPosition
			camera.worldPosition[2] = z_cam + 1
			camera.worldPosition += pos


	def targetMovement(self, player):
		"""
		Target movement force, strafe, roll, etc
		"""
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

	def setupTargetObject(self):
		"""
		Setup data when have target object (cam position, player orient, etc)
		"""
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

	def update(self):
		# Parry manager
		# Test if can parry
		self.canParry()
		if (self.parry):
			if (self.parryTime < 5.0):
				if (self.targetObject != None and self.targetObject.attackLevel == 0):
					self.deactivateParry()
					self.parryTime = 0.0
				else:
					self.parryTime += 0.1
			else:
				self.deactivateParry()
				self.parryTime = 0.0
