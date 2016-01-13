from bge import logic

def stop_target(cont):
    track = cont.actuators['track']
    track.object = None
    cont.deactivate(track)
    
def target(cont, obj, axis):
    track = cont.actuators['track']
    track.object = obj
    track.trackAxis = axis
    cont.activate(track)

def go_to_point(own, cont):
    pos = own.worldPosition
    start = own['start_point_obj'].worldPosition
    
    own.linearVelocity[0] = 0.0
    
    if ((pos[0] >= start[0] - 2  and pos[0] <= start[0] + 2)
        and (pos[1] >= start[1] - 2 and pos[1] <= start[1] + 2)):
        own.linearVelocity[1] = 0.0
        return True
    else :
        target(cont, own['start_point_obj'], 1)
        own.linearVelocity[1] = 2.5
        cont.activate('run')
        step_run_sound(cont)
        return False
    
def go_to_player(own, cont, player):
    ray = cont.sensors['ray_player']
    
    own.linearVelocity[0] = 0.0
    
    if detect_empty_space(own, cont):
        if (ray.positive):
            own.linearVelocity[1] = 0.0
            return True
        else :
            target(cont, player, 1)
            own.linearVelocity[1] = 5.0
            cont.activate('run')
            step_run_sound(cont)
            return False
    else:
        #go to reset
        own.state = logic.WOLFOS_RESET
        return

def detect_empty_space(own, cont):
    ground_ray = cont.sensors['ground_ray']
    if (ground_ray.positive):
        return True
    else :
        return False

def limit_test(own, cont):
    pos = own.worldPosition
    limit = own['zone'].worldPosition
    if ((pos[1] >= limit[1]+15 or pos[1] <= limit[1]-15)
        or (pos[0] >= limit[0]+15 and pos[0] <= limit[0]-15)):
        return True
    else :
        return False

def step_run_sound(cont):
    frame = cont.actuators['run'].frame
    if ((frame >= 41 and frame <= 43)):
        cont.activate('step')