from bge import logic

def open(cont):
    own = cont.owner
    logic.globalDict['Chests'][own['key']] = True
