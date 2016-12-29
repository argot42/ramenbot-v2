import commanderror

class Command:
    def __init__(self, name, function, args, sender, receiver, db):
        self.name = name
        self.function = function        # a python function
        self.args = args                # a list of arguments
        self.sender = sender            # who sent the msg
        self.receiver = receiver        # who got the msg (usr or chan)
        self.database = db              # a instance of DBM


    def execute(self):
        try:
            return self.function({"arguments": self.args, "sender": self.sender, "receiver": self.receiver, "database": self.database}) 
        except:
            raise commanderror.CommandException("External command error")
