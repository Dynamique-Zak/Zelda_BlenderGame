import os
import sys

class color:
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Message:
    @staticmethod
    def printMessage(self, message):
        print(message)

    @staticmethod
    def printOkMessage(message):
        print(color.OKGREEN + message  + color.ENDC)

    @staticmethod
    def printInfoMessage(message):
        print(color.OKBLUE + message  + color.ENDC)

    @staticmethod
    def printFailMessage(message):
        print(color.FAIL + message  + color.ENDC)
