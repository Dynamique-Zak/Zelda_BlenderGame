#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from dx_bge.conf import DX_BGE
from dx_bge.CmdUtils import *
from dx_bge.WriteUtils import *

class Comment:
    IMPORT_INFO = "# Import modules \n"

    STARTER_PART = "# ---------------------------------------------------------------------\n" \
    "# * Starters\n" \
    "# ---------------------------------------------------------------------\n"

    STATES_PART = "# ---------------------------------------------------------------------\n" \
    "# * States\n" \
    "# ---------------------------------------------------------------------\n"

class StateWriting:
    BASE_PATH = os.getcwd()

    @staticmethod
    def getStarterStateFunctionStr(etat, functionName):
        return "def start_" + functionName + etat + "State(self):\n" \
        '\t""" \n\tDocumentation \n\t"""\n' \
        "\tself.switchState(PlayerState." + StateWriting.getStateFunctionConstantName(etat, functionName) + ")"

    @staticmethod
    def getFunctionStateFunctionStr(name):
        return "def " + name + "State(self):\n" \
        '\t""" \n\tDocumentation \n\t"""\n' \
        "\tpass"

    @staticmethod
    def getCompleteFunctionName(etat, functionName):
        """ Return complete function name
        Exemple: waitPushState
        """
        return functionName + etat + "State"

    @staticmethod
    def getStateFilename(name):
        """ Return state constants filename (states/myState.py)
        """
        return StateWriting.BASE_PATH + "/chars/" + DX_BGE.PLAYER_SCRIPT_PATH + "/states/" + name + ".py"

    @staticmethod
    def getStatesConstantsFilename():
        """ Return state constants filename (PlayerConstants.py)
        """
        return StateWriting.BASE_PATH + "/chars/" + DX_BGE.PLAYER_SCRIPT_PATH + "/PlayerConstants.py"

    @staticmethod
    def getStateManagementFilename():
        """ Return state constants filename (PlayerStateManagement.py)
        """
        return StateWriting.BASE_PATH + "/chars/" + DX_BGE.PLAYER_SCRIPT_PATH + "/PlayerStateManagement.py"

    @staticmethod
    def getStateFunctionConstantName(etat, functionName):
        """ Return state constant name from etat and function name
        Keyword arguments:
        etat -- the state name (parent of functionName). Exemple: Idle
        functionName -- the function state name. Exemple: wait -> waitIdleState() and for constants -> WAIT_IDLE_STATE
        """
        return functionName.upper() + "_" + etat.upper() + "_STATE"

    @staticmethod
    def isStateConstant(string):
        """ Test if current string is a state constant and return True if is all right
        Keyword arguments:
        string -- The state constant in string
        """
        if ( "_STATE " in string ):
            return True
        else:
            return False

    @staticmethod
    def create_player_state(name):
        """ Create a new state into states python files
        Keyword arguments:
        name -- the state name (parent of functionName). Exemple: Push for pushing bloc ability of a player.
            The name of state python file. Exemple Push.py
        """
        filename = StateWriting.getStateFilename(name)
        # Create states file
        try:
            file = open(filename, "w")
            # Write default
            file.write(WriteUtils.getHeaderScript() + "\n") # Import basic state
            file.write(Comment.IMPORT_INFO + "from link_scripts.PlayerConstants import PlayerState\n") # Import basic state
            file.write(Comment.STARTER_PART) # Write Starter Part
            file.write(Comment.STATES_PART) # Write States Part
            file.close()
            Message.printOkMessage("L'etat " + name + " du joueur a été crée !")
        except:
            Message.printFailMessage("Impossible de créer l'état")

    @staticmethod
    def add_player_state_function_constant(etat, functionName):
        """ Add state function of player
        Exemple of function name generation : myfunctionEtatState(self)

        Keyword arguments:
        etat -- the state name (parent of functionName). Exemple: Idle
        functionName -- the function state name. Exemple: wait -> waitIdleState() and for constants -> WAIT_IDLE_STATE
        """
        filename = StateWriting.getStatesConstantsFilename()
        # open
        try:
            # Init modified content
            new_content = ""
            # Get constant name generation
            constantName = StateWriting.getStateFunctionConstantName(etat, functionName)
            partName = "# " + etat + " State"
            counterState = 0
            haveStatePart = False
            haveStateFunction = False
            # Error when copy
            success = False

            # Read file content for future modification
            with open(filename, "r") as myFile:
                lines = myFile.readlines()

                # Search State part and Constant name
                for line in lines:
                    if partName in line:
                        haveStatePart = True
                    if constantName in line:
                        haveStateFunction = True
                    # If detect a state add to the counter
                    if ( StateWriting.isStateConstant(line) ):
                        counterState += 1

            # Copy and edit if constant function doesn't exist
            if not haveStateFunction:
                current_value = 0
                # Open file for copy
                with open(filename, "r") as myFile:
                    lines = myFile.readlines()
                    i = 0

                    for line in lines:
                        # If state part already exists
                        if (haveStatePart):
                            # If find part, add constant after this part
                            if (partName in line):
                                line += "\t" + constantName + " = " + str(counterState) + "\n"
                                success = True
                        else:
                            # Get next line for add the new content
                            if not ("# * End Constants" in line):
                                next_line = lines[i+1]
                                # Edit current state value
                                if ( StateWriting.isStateConstant(line) ):
                                    pos = line.find("=")
                                    new_line = line[0:pos] + "= " + str(current_value) + "\n"
                                    line = new_line
                                    current_value += 1

                                # Create part state and add the new content
                                if ("# * End Constants" in next_line):
                                    line += "\t" + partName + "\n\t" + constantName + " = " + str(counterState) + "\n"
                                    success = True
                        # add line to content
                        new_content += line
                        # Increment
                        i += 1
                # Open and write the new file
                if (success):
                    with open(filename, "w") as myFile:
                        myFile.write(new_content)
                else:
                    Message.printFailMessage("Impossible d'ajouter la constante " + constantName, ", une erreur persiste !")
            # If constant already exists print info message
            else:
                Message.printInfoMessage("Impossible d'ajouter la constante " + constantName + ", elle existe déjà !")

        except:
            Message.printFailMessage("Impossible d'ajouter la constante " + constantName)

    @staticmethod
    def addPlayerStateFunctionInStateManager(etat, functionName):
        """ Add the function state into PlayerStateManagement

        Keyword arguments:
        etat -- the state name (parent of functionName). Exemple: Idle
        functionName -- the function state name. Exemple: wait -> waitIdleState() and for constants -> WAIT_IDLE_STATE
        """
        filename = StateWriting.getStateManagementFilename()
        # open
        try:
            # Init variable
            stateIsAlwaysImported = False
            stateFunctionAlreadyExists = False
            successCopy = False
            # Get constant name of the current function state
            constantName = StateWriting.getStateFunctionConstantName(etat, functionName)
            new_content = ""
            complete_function_name = StateWriting.getCompleteFunctionName(etat, functionName)

            # Read file content for future modification
            with open(filename, "r") as myFile:
                lines = myFile.readlines()

                # * Validation search existed content
                for line in lines:
                    # If detect state importation
                    if "from link_scripts.states." + etat + " import *" in line:
                        stateIsAlwaysImported = True
                    # If detect function state declaration
                    if "elif (etat == PlayerState." + constantName + "):" in line:
                        stateFunctionAlreadyExists = True
                        Message.printInfoMessage(complete_function_name + " existe déjà")

                # Search State part and Constant name
                for line in lines:
                    # If state isn't imported into the script
                    if ( not stateIsAlwaysImported):
                        if "# Import states" in line:
                            line += "from link_scripts.states." + etat + " import *\n"

                    # If detect ending of state management can add new state function
                    if ( not stateFunctionAlreadyExists and ("# * End State Management" in line) ):
                        old = "" + line
                        # Edit the new line
                        line = "\n\telif (etat == PlayerState." + constantName + "):\n" \
                    		"\t\t" + complete_function_name + "(player)\n" + old
                        # Set successCopy True
                        successCopy = True
                    # Copy line
                    new_content += line

            # Open and write the new file if successCopy is True
            if (successCopy):
                with open(filename, "w") as myFile:
                    myFile.write(new_content)
                # Ok message
                Message.printOkMessage(complete_function_name + " à été ajoutée avec succès !")
            else:
                if (not stateFunctionAlreadyExists):
                    # Fail message
                    Message.printFailMessage("Impossible d'ajouter " + complete_function_name + " dans PlayerStateManagement")
        except:
            pass

    @staticmethod
    def add_player_state(etat, functionName):
        """ Add a player state function
        Exemple: waitPushState

        Keyword arguments:
        etat -- the state name (parent of functionName). Exemple: Push
        functionName -- the function state name. Exemple: wait -> waitPushState() and for constants -> WAIT_PUSH_STATE
        """
        filename = StateWriting.getStateFilename(etat)
        # open
        try:
            success = 0
            new_content = ""

            # Read file content for future modification
            with open(filename, "r") as myFile:
                lines = myFile.readlines()
                i = 0
                # Names
                starter_function_str = StateWriting.getStarterStateFunctionStr(etat, functionName)
                function_str = StateWriting.getFunctionStateFunctionStr(functionName + etat)
                # Test variables
                starterFunctionAlreadyExists = False
                functionAlreadyExists = False

                # Verify if functions doesn't exists
                starter_function_name = "start_" + functionName + etat + "State"
                function_name = functionName + etat + "State"

                for line in lines:
                    if starter_function_name in line:
                        starterFunctionAlreadyExists = True
                    if function_name in line:
                        functionAlreadyExists = True

                # Print message
                if (starterFunctionAlreadyExists):
                    Message.printInfoMessage("Le starter " + starter_function_name + " existe déjà")
                if (functionAlreadyExists):
                    Message.printInfoMessage("La fonction " + function_name + " existe déjà")

                # Now copy
                for line in lines:
                    # Add starter state
                    if ( line.startswith("# * Starters") and not starterFunctionAlreadyExists ):
                        lines[i+1] += starter_function_str + "\n\n"
                    elif (line.startswith("# * States") and not functionAlreadyExists ):
                        lines[i+1] += function_str + "\n\n"

                    new_content += line
                    i += 1;
            # Now open file for modification
            with open(filename, "w") as myFile:
                myFile.write(new_content)

            # Add constants
            StateWriting.add_player_state_function_constant(etat, functionName)
            StateWriting.addPlayerStateFunctionInStateManager(etat, functionName)

            # Si il a eu modification
            if (starterFunctionAlreadyExists or functionAlreadyExists ):
                Message.printOkMessage("L'état " + etat +" à été mise à jour")
            else:
                Message.printOkMessage(functionName + " de l'etat " + etat +" à été ajoutée avec succès !")
        except:
            Message.printFailMessage("Impossible d'ajouter " + functionName + " dans l'état " + etat)
