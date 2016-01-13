class PlayerCam:

	def __init__(self, player, camera):
		self.player = player
		self.cam = camera

	def camToFirstview(self):
		# deactivate the tracked mode
		self.cam['tracked_player'] = False
		# set pos to the first view pos
		#self.cam.worldPosition = self.player.first_view_obj.worldPosition
		# set orientation to the first view pos
		#self.cam.orientation = self.player.first_view_obj.orientation
		# set parent
		#self.cam.setParent(self.player.first_view_obj, False)

	def deactiveTrackPlayer(self):
		self.cam['tracked_player'] = False

	def activeTrackPlayer(self):
		# deactivate the tracked mode
		self.cam['tracked_player'] = True

	def activeLookPlayer(self):
		self.cam['look_player'] = True

	def deactiveLookPlayer(self):
		self.cam['look_player'] = False

	def applyLook(self, UpDown, LeftRight):
		# test limit
		next_rot = self.player.first_view_obj.orientation.to_euler()[0] + UpDown

		#if (next_rot < 3.2 and next_rot > 0.0):
		# apply up down rotation
		self.player.first_view_obj.applyRotation([UpDown, 0, 0], 1)
		# apply left right rotation
		self.player.applyRotation([0, 0, LeftRight], 1)

		# apply transform
		self.cam.worldPosition = self.player.first_view_obj.worldPosition
		self.cam.orientation = self.player.first_view_obj.orientation

	def cameraViewControl(self, gamepad):
		axis = gamepad.getJoyAxis2()
		x_move = axis[1]
		self.cam.applyMovement([x_move, 0, 0], 1)
