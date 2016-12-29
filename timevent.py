class Timevent:
    """ events triggered by time """

    def __init__(self, state, init_time, end_time, command):
        self.running = state
        self.init_time = init_time
        self.end_time = end_time
        self.command = command

        # update
        self.updated_time = init_time


    def reset(self):
        self.updated_time = self.init_time


    def disable(self):
        self.running = False


    def enable(self):
        self.running = True


    def update(self, time):
        self.updated_time += time


    def is_time(self):
        #print(self.updated_time, "::::", self.end_time)
        return self.end_time <= self.updated_time


    def execute(self):
        return self.command.execute()
