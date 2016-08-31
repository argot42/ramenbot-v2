import re

class Parser:
 #   def __init__(self, *irc_commands, **regex_dict):
        #self.regex = dict()

        #try:
        #    for name, regex_tuple in regex_dict.items():
        #        self.regex[name] = re.compile(regex_tuple[0], regex_tuple[1])   # regex_tuple[0] = regex string | regex_tuple[1] = option int
        #                            
        #except:
        #    raise

    def parse_msg(msg):
        user = str()
        tail = list()

        if not msg: return None, None, None

        if msg[0] == ':':
            user, msg = msg[1:].split(' ', 1)

        if msg.find(' :') != -1:
            msg, tail = msg.split(' :', 1)
            args = msg.split()
            args.append(tail)
        else:
            args = msg.split()

        command = args.pop(0)

        return user, command, args
