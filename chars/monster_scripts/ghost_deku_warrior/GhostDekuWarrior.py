from bge import logic
from monster_scripts.Monster import *
from monster_scripts.ghost_deku_warrior.GhostDekuWarriorRig import *
from monster_scripts.ghost_deku_warrior.GhostDekuWarriorStates import statesManager

class GhostDekuWarrior(Monster):

	def __init__(self, own, mesh, rig, attackBox):
		Monster.__init__(self, own, mesh, rig, attackBox)
		self.rig = GhostDekuWarriorRig(rig)
		self.etat = 1

	def main(self):
		statesManager(self)

def main(cont):
	own = cont.owner

	if not 'init' in own:
		mesh = None
		rig = None
		attackBox = None

		# Get rig and mesh obj
		for obj in own.children:
			if obj.name == "gdw_rig":
				rig = obj

		for obj in rig.children:
			if obj.name == "gosht_deku_warrior_mesh":
				mesh = obj
			if obj.name == "gkw_sword_bound":
				attackBox = obj

		# Make monster
		own = GhostDekuWarrior(own, mesh, rig, attackBox)
		# Ok
		own['init'] = True
	else:
		own.main()
