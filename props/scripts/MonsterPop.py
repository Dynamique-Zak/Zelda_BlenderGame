from bge import logic
import mathutils

scene = logic.getCurrentScene()

def pop(cont):
	own = cont.owner
	# add obj
	for i in range(0, 12):
		# Get position of origin object
		pos = mathutils.Vector(own.worldPosition)
		pos[0] = (own.worldPosition[0]) + own['x']
		pos[1] = (own.worldPosition[1]) + own['y']
		# Rotate vector
		pos.rotate(own.orientation)
		# Add object
		dust = scene.addObject("dust1", own, 80)
		# Set new transformation
		dust.worldPosition = pos
		# Create range
		nxRange = range(3, 6)
		nxRange2 = range(7, 9)
		nyRange = range(7, 12)
		space = 0.1

		# Increment etc.
		if (i == 6):
			own['x'] = -space
			own['y'] = (own['startY'] * -1) + space
		else:
			# increment x
			if (i in nxRange or i in nxRange2):
				own['x'] -= space
			else:
				own['x'] += space
			# increment y
			if (i in nyRange):
				own['y'] -= space
			else:
				own['y'] += space
