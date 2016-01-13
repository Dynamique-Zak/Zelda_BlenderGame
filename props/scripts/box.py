from bge import logic

def main(cont):
    own = cont.owner
    collid_test = cont.sensors['collid_test']
    if collid_test.positive:
        own['collid'] = True
    else :
        own['collid'] = False