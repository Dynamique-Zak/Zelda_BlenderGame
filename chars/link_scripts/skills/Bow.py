from bge import logic

class BowContainer:
    def __init__(self, number, max):
        # if bowContainer not exist init then
		if not 'bowContainer' in logic.globalDict['Player']:
			logic.globalDict['Player']['bowContainer'] = {'arrow' : number, 'maxArrow' : max}

    def use(self, quantity):
        """
		Lost heart, if the lose exceeds then set to zero
		"""
		bowContainer = logic.globalDict['Player']['bowContainer']
		next_arrow = heartContainer['arrow'] - quantity
		if (next_heart < 0):
			heartContainer['arrow'] = 0
		else:
			heartContainer['arrow'] = next_arrow

class Bow:
    def __init__(self):
        self.container = BowContainer(10, 30)
