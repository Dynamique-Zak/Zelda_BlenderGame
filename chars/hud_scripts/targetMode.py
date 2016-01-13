from bge import logic

cont = logic.getCurrentController()

def main(cont):
    own = cont.owner
    try :
        if (logic.globalDict['target_mode']):
            cont.deactivate('no_active')
            cont.activate('active')
            if (own['target'] == False):
                cont.activate('target_sound')
                own['target'] = True
        else :
            cont.deactivate('active')
            cont.activate('no_active')
            own['target'] = False
    except :
        pass

main(cont)