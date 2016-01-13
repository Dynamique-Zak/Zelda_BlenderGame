from bge import logic

scene = logic.getCurrentScene()

class PlayerFightManager:

    def __init__(self, player):
        self.player = player

    def switchSwordAndShield(self):
        sword = scene.objects["sword"]
        shield = scene.objects["shield"]
        armed_back = scene.objects["armedBack"]
        shield_back = scene.objects["shield_back"]

        if (self.player.armed):
            # hide active shield and sword
            sword.setVisible(False)
            shield.setVisible(False)
            # hide back
            armed_back.setVisible(True, True)
        else:
            # Display
            sword.setVisible(True)
            shield.setVisible(True)
            # hide back
            armed_back.setVisible(False, True)
