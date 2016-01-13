from bge import logic, events, types

class Monster(types.KX_GameObject):
    
    def __init__(self, hp):
        self['monster'] = True
        self.alive = True
        self.hp = hp