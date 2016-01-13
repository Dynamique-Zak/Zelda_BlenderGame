from bge import logic, types, events

scene = logic.getCurrentScene()
cont = logic.getCurrentController()
objects = scene.objects

def main(cont):
	own = cont.sensors['lensFlare'].owner

	if 'cam_player' in logic.globalDict:
	   own.worldPosition = logic.globalDict['cam_player'].worldPosition
	   own.orientation = logic.globalDict['cam_orient']

	if 'SunPos' in logic.globalDict and own['ok'] == False:
		print('lol le soleil')
		# set parent
		objects["sunPos"].worldPosition = logic.globalDict['SunPos']
		camPlan = cont.sensors['toCamPlan'].owner
		camPlan.worldPosition = logic.globalDict['SunPos']
		own['ok'] = True

main(cont)