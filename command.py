class Command:
    def __init__(self, name, function, args, sender, receiver):
        self.name = name
        self.function = function        # a python function
        self.args = args                # a list of arguments
        self.sender = sender            # who sent the msg
        self.receiver = receiver        # who got the msg (usr or chan)


    def execute(self):
        return self.function(self.args) 
