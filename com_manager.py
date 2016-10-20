import re
import os
import importlib.machinery

from command import Command

class Commanager:
    def __init__(self, path):
        """ When the class is instantiated, it loads all commands (<name>_com_.py) in the directory pointed by 'path' """

        self.path = os.path.expanduser(path)
        self.commands = dict()
        
        files = os.listdir(self.path)
        for f in files:
            match = re.match(r'^(?P<name>\w+)_com_\.py$', f)

            if match: self.commands[match.group("name")] = \
                        getattr(importlib.machinery.SourceFileLoader(\
                            match.group("name"), self.path + '/' + f).load_module(), match.group("name"))


    def mkcom(self, name, args, sender, receiver, db):
        try:
            return Command(name, self.commands[name], args, sender, receiver, db)

        except KeyError:
            return None
