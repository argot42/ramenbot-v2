class Parser:
    def parse_msg(msg):
        """ substring approach for parsing irc msg """

        if not msg: raise RuntimeError
        msg = msg.replace('\r', '')

        if msg[0] != ':': 
            command, arguments = msg.split(':')
            return '', '', command.replace(' ', ''), arguments

        sender, command, rest = msg[1:].split(' ', 2)

        r_separator = rest.find(':')
        if r_separator < 0: return sender, rest, command, ''

        s_separator = sender.find('!')
        if s_separator > 0: sender = sender[:s_separator]

        return sender, rest[:r_separator], command, rest[r_separator+1:]


    def find_command(irc_args, prefix):
        try:
            if irc_args[0] != prefix:
                return '', '' 
            arguments = irc_args.split(' ')
            command = arguments.pop(0)[1:]

            return command, arguments 

        except IndexError:
            return '', ''
