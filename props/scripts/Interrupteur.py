from bge import types

def active(cont):
    own = cont.owner
    if ( own['active'] == False):
        own['active'] = True
        # Get the bloc
        touchBloc = cont.sensors['touchBloc']
        bloc = touchBloc.hitObject
        # Block the bloc
        bloc.block()
        bloc['bloc'] = False
        # Set bloc to Interrupteur
        bloc.worldPosition[0] = own.worldPosition[0]
        bloc.worldPosition[1] = own.worldPosition[1]
        bloc.worldPosition[2] = own.worldPosition[2] + 0.8
        # Call active function
        own['activeFunction']()
