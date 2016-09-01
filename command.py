class Command:
    def __init__(self, function, args, sender, receiver):
        self.function = function        # a python function
        self.args = args                # a list of arguments
        self.sender = sender            # who sent the msg
        self.receiver = receiver        # who got the msg (usr or chan)


    def exec(self):
        try:
            return self.function(self.args) 

        except:
            raise
