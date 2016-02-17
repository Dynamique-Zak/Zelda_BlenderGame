from bge import logic
from link_scripts.PlayerConstants import ArmAnimation

scene = logic.getCurrentScene()

class PlayerFightManager:

    def __init__(self, player):
        self.player = player
        self.unsheated = False
        self.equipedSword = None
        self.equipedShield = None

    def canUseSword(self):
        can = False
        if ( self.player.inventory.equipAnyEquipementSession('Swords') and self.player.pickManager.active != True ):
            can = True
        return can

    def initEquipement(self):
        self.updateEquipement()
        #self.switchSwordAndShield()

    def isUnsheated(self):
        return self.unsheated

    def isEquiped(self):
        return (self.equipedSword != None or self.equipedShield != None)

    def unsheat(self, active):
        if (self.unsheated != active):
            if ( not self.unsheated ):
                self.unsheated = True
                self.switchSwordAndShield()
            else:
                self.unsheated = False
                self.switchSwordAndShield()

    def updateEquipement(self):
        # swords
        for id_sword, sword in self.player.inventory.getEquipementSession("Swords").items() :
            if (sword['equiped']):
                self.equipedSword = id_sword
        # shields
        for id_shield, shield in self.player.inventory.getEquipementSession("Shields").items() :
            if (shield['equiped']):
                self.equipedShield = id_shield
        # Switch
        self.switchSwordAndShield()

    def switchSwordAndShield(self):
        # Get armed objects
        armed_back = scene.objects['armedBack']

        if (self.equipedSword != None):
            sword = scene.objects["player." + self.equipedSword]
            sword_back = scene.objects["player." + self.equipedSword + ".back"]
            sword_sheath = scene.objects["player." + self.equipedSword + ".sheath"]
        if (self.equipedShield != None):
            shield = scene.objects["player." + self.equipedShield]
            shield_back = scene.objects["player." + self.equipedShield + ".back"]

        # Sword sheath set
        if ( self.equipedSword):
            if (not sword_sheath.visible):
                sword_sheath.setVisible(True)
        else:
            sword_sheath.setVisible(False)
            
        # If is unsheated
        if ( self.unsheated ):
            # go to armed arm animation
            self.player.rig.setArmAnimation(ArmAnimation.ARMED)
            # hide active shield and sword
            if (self.equipedSword != None):
                sword.setVisible(True)
                sword_back.setVisible(False)
            if (self.equipedShield != None):
                shield.setVisible(True)
                shield_back.setVisible(False)
        # Is just equiped
        elif ( self.isEquiped() ):
            # go to normal arm animation
            self.player.rig.setArmAnimation(ArmAnimation.NORMAL)
            # Display
            if (self.equipedSword != None):
                # Hide forward sword
                sword.setVisible(False)
                # Display backward sword
                sword_back.setVisible(True)
            if (self.equipedShield != None):
                # Hide forward sword
                shield.setVisible(False)
                # Display backward shield
                shield_back.setVisible(True)
