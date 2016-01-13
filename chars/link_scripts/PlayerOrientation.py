from bge import logic
import math
import mathutils

scene = logic.getCurrentScene()

class PlayerOrientationManager:
	def __init__(self):
		pass

	def linearOrient(player, target):
		pass

	def orient_player(self, player):
		if (player.targetManager.active == False):
			orientController = scene.objects['orientController']

			x_axis = player.gamepad.getJoyAxis1()[0]
			y_axis = player.gamepad.getJoyAxis1()[1]

			angle_radians = math.atan2(x_axis, y_axis)
			angle_degrees = math.degrees(math.atan2(y_axis,x_axis))

			baseZ = orientController.worldOrientation.to_euler()[2]
			xyz = player.worldOrientation.to_euler()
			rotz = math.degrees(xyz[2])
			xyz[2] = (baseZ-math.pi) + angle_radians
			xyz.to_matrix()

			player.worldOrientation = xyz

	def updateOrientController(self, pos, orient):
		orientController = scene.objects['orientController']
		orientController.worldPosition = pos
		orientController.worldOrientation = orient

	def stopOrientation(self, player):
		player.setTrackOrient(None)
