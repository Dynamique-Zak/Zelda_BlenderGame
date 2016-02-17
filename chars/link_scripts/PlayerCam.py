from bge import logic
import mathutils

class PlayerCamAnimation:
	GET_ITEM = "CAMPOSITION:GET_ITEM"
	DEATH = "CAMPOSITION:DEATH"

class PlayerCam:

	def __init__(self, player, camera):
		self.player = player
		self.cam = camera
		self.camAnimation = False

	def camToFirstview(self):
		# deactivate the tracked mode
		self.cam['tracked_player'] = False

	def activeCamAnimation(self, message):
		if (self.camAnimation != True):
			# Copy pos to the camera before the animation
			scene = logic.getCurrentScene()
			cam_pos = scene.objects['cam.position']
			cam_pos.worldPosition = self.cam.worldPosition
			# Active
			self.camAnimation = True
			self.deactiveTrackPlayer()
			logic.sendMessage(message)

	def deactivateCamAnimation(self):
		self.camAnimation = False
		self.activeTrackPlayer()

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

		# apply up down rotation
		self.player.first_view_obj.applyRotation([UpDown, 0, 0], 1)
		# apply left right rotation
		self.player.applyRotation([0, 0, LeftRight], 1)

		# apply transform
		self.cam.worldPosition = self.player.first_view_obj.worldPosition
		self.cam.orientation = self.player.first_view_obj.orientation

	def setCameraAfterDoorClose(self):
		player_pos = self.player.worldPosition
		pos = mathutils.Vector([5, 5, 0])
		pos.rotate(self.player.orientation)
		new_pos = pos + player_pos
		self.cam.worldPosition = new_pos

	def cameraToBackPlayer(self):
		pos = mathutils.Vector([0, -9, 2])
		pos.rotate(self.player.orientation)
		new_pos = pos + self.player.worldPosition
		if ( logic.camObstaclePosition == None):
			self.cam.worldPosition = new_pos

	def cameraViewControl(self, gamepad):
		axis = gamepad.getJoyAxis2()
		x_move = axis[1]
		self.cam.applyMovement([x_move, 0, 0], 1)

	def main(self):
		scene = logic.getCurrentScene()
		cam_pos = scene.objects['cam.position']
		if ( self.camAnimation ):
			self.cam.worldPosition = cam_pos.worldPosition
			self.cam.worldOrientation = cam_pos.worldOrientation.to_euler()
