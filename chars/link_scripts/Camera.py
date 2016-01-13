from bge import logic

def obstacle(cont):
	ray = cont.sensors["RayForward"]
	
	if ray.positive:
		hitObj = ray.hitObject
		if hitObj.name != "Link":
			cam = cont.sensors["backCam_sensors"].owner
			cam.worldPosition = ray.hitPosition
