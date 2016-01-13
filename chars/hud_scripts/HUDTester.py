from bge import logic
from hud_scripts.Gamepad import Gamepad
from hud_scripts.MessageBox import MessageBoxMode

scene = logic.getCurrentScene()

def test(cont):
    own = cont.owner
    inventory = scene.objects['Inventory']

    if not 'init' in own:
        # init fake Player
        logic.globalDict['Player'] = {}

        # init fake heart
        logic.globalDict['Player']['heartContainer'] = {'heart' : 5, 'maxHeart' : 5}

        # init fake rupee
        logic.globalDict['Player']['rupeeContainer'] = {'rupee' : 5, 'maxRupee' : 99}
        logic.globalDict['Player']['Gamepad'] = Gamepad()

        from hud_scripts.HUD import PlayerHUD
        from hud_scripts.MessageBox import MessageBox
        from hud_scripts.Inventory import Inventory

        # Instance
        msgBox = MessageBox(scene.objects['MessageBox'])
        own = PlayerHUD(own, msgBox)

        # Inventory
        inventory = Inventory(scene.objects['Inventory'])

        #msgBox.setText("Quisque maximus odio nec est efficitur, sit amet feugiat dui aliquam. Praesent dapibus, sem sed auctor venenatis, lorem justo maximus risus, eget dignissim dolor elit id nibh! Curabitur nec interdum orci. Sed ut turpis sagittis, semper orci sed, ullamcorper purus. ")

        # Update
        own.updateRupee()
        own.updateHeart()

        # init
        own['init'] = True
        # active it
        #cont.activate('mainState')
    else:
        # update contro ltest
        gamepad = logic.globalDict['Player']['Gamepad']
        if (gamepad.isAttackPressed() and own.messageBox.active == False):
            own.messageBox.displayText("Quisque maximus odio nec est efficitur, sit amet feugiat dui aliquam. Praesent dapibus, sem sed auctor venenatis, lorem justo maximus risus, eget dignissim dolor elit id nibh! Curabitur nec interdum orci. Sed ut turpis sagittis, semper orci sed, ullamcorper purus. ",
            MessageBoxMode.WAIT_INPUT_TYPE)
        # update
        own.main()
        # update inventory
        inventory.main()
