from bge import logic

scene = logic.getCurrentScene()

def touchPlayer(cont):
    own = cont.owner
    sens = cont.sensors['touchPlayer']
    if (sens.positive):
        sens.hitObject.rupeeContainer.gainRupee(own['rupee'])
        scene.addObject("get_rupee_effect", own, 30)
        own.endObject()

def touchGround(cont):
    own = cont.owner
    own.suspendDynamics()
    own.worldPosition[2] += 0.1
    own['dynamics'] = False

def dynamics(cont):
    own = cont.owner

    if not 'init' in own:
        own.restoreDynamics()
        own.linearVelocity[2] += 5.0
        own['init'] = True
