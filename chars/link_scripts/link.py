from bge import logic

scene = logic.getCurrentScene()

def main(cont):
	own = cont.sensors['player'].owner
	cam = cont.sensors['backCam_sensors'].owner
	logic.globalDict['cam_player'] =  cam
	logic.globalDict['cam_orient'] =  scene.objects['camOrient'].orientation
	own.main(cont)
	