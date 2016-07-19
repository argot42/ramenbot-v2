import sys, socket, ssl, time
from os.path import expanduser
from multiprocessing import Process, Lock, Queue

#from ramen import Ramen
#from chopsticks import Chopsticks
from ramenutils import RETRY_DELAY, RETRY_TIMES, MULTI, N_CONSUMER, N_PRODUCER

#import bowlerror

class Bowl:
    def __init__(self, host, port, nick, channels, database, prefix, password, ssl):
        self.host = Bowl.check_host(host)
        self.port = Bowl.check_port(port)
        self.nick = Bowl.check_nick(nick)
        self.channels = Bowl.check_channels(channels)
        self.database = Bowl.check_database(database)
        self.prefix = Bowl.check_prefix(prefix)
        self.password = Bowl.check_password(password)
        self.ssl = Bowl.check_ssl(ssl)

        # create database
        #chop = Chopsticks(self.database)
        #setup db table structure
        #chop.setup()
        

    def connect(self):
        """ Main connection structure. Socket generation and check on connection status """

        for retry_n in range(RETRY_TIMES):
            try:
                ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ircsock.connect((self.host, self.port))

                if self.ssl:
                    print("ssl")

                self.server_login(ircsock)
                self.chan_join(ircsock)

                if MULTI:
                    # multiprocess ramenbot
                    self.start_multi(ircsock)
                else:
                    # single process ramenbot
                    self.start_single(ircsock)
            except:
                raise

            time.sleep(RETRY_DELAY * (retry_n + 1))


    def server_login(self, ircsock):
        """ Connects to the irc server and if you set up a password it logs to NickServ """

        ircsock.send(bytes("USER {} {} {} :xxxx\n".format(self.nick, self.nick, self.nick), "UTF-8"))
        time.sleep(.5)

        ircsock.send(bytes("NICK {}\n".format(self.nick), "UTF-8"))
        time.sleep(.5)

        if self.password:
            print("pass")
            

    def chan_join(self, ircsock):
        print("Joining Chans...")

        for chan in self.channels: ircsock.send(bytes("JOIN {}\n".format(chan), "UTF-8"))


    def ping(self, ircsock, arg):
        print("Pong!")
        ircsock.send(bytes("PONG :{}\n".format(arg), "UTF-8")) 



    ################################### multi process ##########################################
    ############################################################################################

    def start_multi(self, ircsock):
        """ Start main bot function [obtain msg, store command] / [execute command, send output back] that supports multiprocess """      
        
        process_pool = []
        producer_lock = Lock()
        consumer_lock = Lock()
        msg_queue = Queue()

        # generating producers
        for i in range(PRODUCER_N): process_pool.append(Process(target=self.listening, args=(ircsock, consumer_lock, queue,)))

        # generating consumers
        for i in range(CONSUMER_N): process_pool.append(Process(target=self.answering, args=(ircsock, producer_lock, queue,)))

        # start
        for proc in process_pool:
            proc.start()


    def listening(self, ircsock, consumer_lock, queue):
        """ Obtain msg, queue command [producer] """

        consumer_lock.acquire()

        # get msg
        msg = self.get_msg(ircsock)
        # extract command
        command = self.get_comm(msg)

        if type(command) == 'ping':
            self.ping(ircsock, command.argument)

        elif type(command) == 'kick':
            print("KICKED")

        else:
            queue.put(command)
            consumer_lock.release()
        

    def answering(self, ircsock, producer_lock, queue):
        """ Get command, execute it, and send back the output """

        producer_lock.acquire()

        if queue.qsize() != 0:
            command = queue.get()
            response = self.execute(command)

            self.send(response)

        producer_lock.release()
        time.sleep(5)


    ############################################################################################
    ############################################################################################


    ################################### single process #########################################
    ############################################################################################

    def start_single(self, ircsock):
        return True


    ############################################################################################
    ############################################################################################


    ################################# atribute checking ########################################
    ############################################################################################

    def check_host(host):
        return host

    def check_port(port):
        return port

    def check_nick(nick):
        return nick

    def check_channels(channel):
        return channel

    def check_database(database):
        return database

    def check_prefix(prefix):
        return prefix

    def check_password(password):
        return password

    def check_ssl(ssl):
        return ssl
              
    ############################################################################################
    ############################################################################################
