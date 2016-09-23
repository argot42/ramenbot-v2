class IRCError(Exception):
    """ Base class """

    pass


class IRCShutdown(IRCError):
    """ IRC server close connection """

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return repr(self.description)
