#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re

from dx_bge.StateWriter import *

class CommandMatch:
    STATE_COMMAND_REGEX = re.compile(r"player_state:([a-zA-Z]):([a-zA-Z]):([a-zA-Z0-9])")


def execute(args):
    command_name = args[0]

    if (command_name == "create_player_state"):
        name = args[1]
        StateWriting.create_player_state(name)
    else:
        cr = command_name.split(":")
        if(cr[0] == "player_state"):
            # add state
            if cr[1] == "add":
                # get etat
                etat = cr[2]
                # get etat fonctio
                etatFunction = cr[3]
                # add
                StateWriting.add_player_state(etat, etatFunction)

if __name__ == "__main__":
    execute(sys.argv[1:])
