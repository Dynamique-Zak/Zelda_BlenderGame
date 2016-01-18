from bge import logic

scene = logic.getCurrentScene()

def main(cont):
    own = cont.owner
    dist = own.getDistanceTo(scene.active_camera)
    if (own.visible and dist < 30):
        own.setVisible(True, True)
    elif (own.visible == False and dist >= 30):
        own.setVisible(False, True)
