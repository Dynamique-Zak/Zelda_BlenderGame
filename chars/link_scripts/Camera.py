from bge import logic

scene = logic.getCurrentScene()

def obstacle(cont):
	ray = cont.sensors["RayForward"]

	if ray.positive:
		hitObj = ray.hitObject
		if hitObj.name != "Link":
			cam = scene.objects['MainCam']
			cam.worldPosition = ray.hitPosition
