import re
from importlib import import_module
from os import listdir
from os.path import abspath

from command import Command

class Commanager:
    def __init__(self, path):
        self.path = abspath(path)
        self.commands = dict()
        
        files = listdir(self.path)
        for f in files:
            match = re.match(r'^(?P<file>(?P<name>\w+)_com_)\.py$', f)

            if match: self.commands[match.group("name")] = getattr(import_module(match.group("file")), m.group("name"))


    def get_com(self, name, args):
        return Command(self.commands[name], args)
