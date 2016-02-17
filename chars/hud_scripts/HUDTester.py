from bge import logic
from link_scripts.Gamepad import Gamepad
from hud_scripts.MessageBox import MessageBoxMode
from link_scripts.GameInit import initGame
from link_scripts.PlayerInventory import *

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
        # Init game
        initGame()
        logic.inventory = PlayerInventory(None)
        logic.globalDict['Player']['Inventory']['Equipement']['Swords']['basic_sword']['have'] = True
        logic.globalDict['Player']['Inventory']['Equipement']['Swords']['hero_sword']['have'] = True
        logic.globalDict['Player']['Inventory']['Equipement']['Shields']['wood_shield']['have'] = True

        # Real test

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

        own.setMiniMap("dungeon1_enter.png")

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

        if gamepad.isPausePressed() and not inventory.active:
            own.displayInventory()
        elif inventory.active and gamepad.isPausePressed():
            own.closeInventory()

        # update
        own.main()
        # update inventory
        inventory.main()
