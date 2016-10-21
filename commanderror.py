class Err(Exception):
    """ Base class """
    pass


class ComErr(Err):
    """ No command loaded with given name """

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return repr(self.description)


class NoCommandFound(ComErr):
    pass


class CommandException:
    pass
