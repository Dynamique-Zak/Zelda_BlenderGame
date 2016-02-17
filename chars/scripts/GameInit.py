from bge import logic

def addObject(name, id_obj, description, gain_description, type_obj, value):
    logic.globalDict['Objects'].append({'name' : name, 'id_obj' : id_obj, 'description' : description,
    'description2': gain_description, 'type' : type_obj, 'value' : value})

def initGame():
    # Init logic globalDict Object
    logic.globalDict['Objects'] = []
    # Set default obj
    addObject('Rubis vert', 'green_rupee', 'Un rubis vert vaut 1 rubi.', 'Fantastique 1 rubi..... Il y\'a beaucoup mieux c\'est sur...', 1, 1)
