class Command:
    def __init__(self, function, args):
        self.function = function        # a python function
        self.args = args                # a list of arguments


    def exec(self):
        try:
            return self.function(self.args) 

        except:
            raise
