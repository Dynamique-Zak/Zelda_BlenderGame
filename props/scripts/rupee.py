from bge import logic

def main(cont):
    own = cont.owner
    #sens
    collision = cont.sensors['Touch']
    player = logic.globalDict['player']
    fx_rupee = cont.actuators['fx_rupee']
    #
    if collision.positive:
        #
        fx_rupee.object = "fx_get_rupee"
        cont.activate('fx_rupee')
        #add rupee to play
        if player['rupee'] < 99 :
            logic.globalDict['player']['rupee'] += 1
            own.endObject()