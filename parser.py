class Parser:
    def parse_msg(msg):
        """ substring approach for parsing irc msg """

        if not msg: raise RuntimeError

        substr_list = msg.split(':', 2)

        if not substr_list[0] == '': return '', '', substr_list[0], substr_list[1]    # sender, receiver, irc command, arguments

        # catching MOTD and no-command msg
        # TODO find a better way to handle this
        if len(substr_list) < 3: return '', '', '', substr_list[0]

        user_info = substr_list[1].split(' ')


        # sender, receiver, irc_command, arguments
        return user_info[0][:user_info[0].find('!')], \
                user_info[1], \
                user_info[2], \
                substr_list[2]


    def find_command(irc_args, prefix):
        try:
            if irc_args[0] != prefix:
                return '', '' 
            arguments = irc_args.split(' ')
            command = arguments.pop(0)[1:]

            return command, arguments 

        except IndexError:
            return '', ''
