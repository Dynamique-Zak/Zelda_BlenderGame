from bge import logic

scene = logic.getCurrentScene()

class PlayerEffect:

    def addEffectFrame(current_frame, frames, effectFunction):
        for frame in frames:
            r = range(frame-1, frame+1)
            if ( (current_frame >= frame and current_frame <= frame+1)):
                effectFunction()

    def addGrassEffect():
        obj = scene.objects['Link']
        effect = scene.addObject('grassEffect', obj, 30)
        effect.worldPosition[2] -= 0.6
