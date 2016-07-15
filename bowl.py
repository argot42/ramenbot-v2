import sys, socket, ssl, time
from os.path import expanduser

from ramen import Ramen
from chopsticks import Chopsticks
from ramenutils import retry_delay, retry_times

MULTI = True

#import bowlerror

class Bowl:
    def __init__(self, host, port, nick, channel, channels, database, prefix, password, ssl):
        self.host = Bowl.check_host(host)
        self.port = Bowl.check_port(port)
        self.nick = Bowl.check_nick(nick)
        self.channel = Bowl.check_channel(channel)
        self.database = Bowl.check_database(database)
        self.prefix = Bowl.check_prefix(prefix)
        self.password = check_password(password)
        self.ssl = Bowl.check_ssl(ssl)

        # create database
        chop = Chopsticks(self.database)
        #setup db table structure
        chop.setup()
        

    def connect(self):
        """ Main connection structure. Socket generation and check on connection status """

        for retry_n in range(retry_times):
            try:
                ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ircsock.connect((self.host, self.port))

                if self.ssl:
                    print("ssl")

                self.server_login(ircsock)
                self.chan_join(ircsock)

                if MULTI:
                    # multiprocess ramenbot
                    self.start_ramen_generation_consuption(ircsock)
                else:
                    # single process ramenbot
                    self.start_ramen_single(ircsock)
            except:
                raise

            time.sleep(retry_delay * retry_n + 1)


    def server_login(ircsock):
        """ Connects to the irc server and if you set up a password it logs to NickServ """

        ircsock.send(bytes("USER {} {} {} :xxxx\n".format(self.nick, self.nick, self.nick), 'UTF-8'))
        time.sleep(.5)

        ircsock.send(bytes("NICK {}\n".format(self.nick)))
        time.sleep(.5)

        if self.password:
            print("pass")
            

    def chan_join(ircsock):
        # TODO
        return True


    def start_ramen_generation_consuption(ircsock):
        # TODO
        return True


    def start_ramen_single(ircsock):
        # TODO
        return True


    ################################# atribute checking ########################################
    ############################################################################################
   

    def check_host(host):
        if type(host) != str:

    def check_port(port):
        return True

    def check_nick(nick):
        return True

    def check_channel(channel):
        return True

    def check_database(database):
        return True

    def check_prefix(prefix):
        return True

    def check_password(password):
        return True

    def check_ssl(ssl):
        return True
              

    ############################################################################################
    ############################################################################################
