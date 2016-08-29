import re
from importlib import import_module
from os import listdir

from command import Command

class Commanager:
    def __init__(self):
        """ When the class is instantiated, it loads all commands in the directory the symlink 'com' points to """

        self.path = "com"
        self.commands = dict()
        
        files = listdir(self.path)
        for f in files:
            match = re.match(r'^(?P<file>(?P<name>\w+)_com_)\.py$', f)

            if match: self.commands[match.group("name")] = getattr(import_module("com." + match.group("file")), match.group("name"))


    def get_com(self, name, args):
        return Command(self.commands[name], args)

