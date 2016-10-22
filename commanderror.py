class Err(Exception):
    """ Base class """
    pass


class ComErr(Err):
    """ Commands error class """

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return repr(self.description)


class NoCommandFound(ComErr):
    pass


class CommandException:
    pass
