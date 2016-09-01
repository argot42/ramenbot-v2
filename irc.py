import sys, socket, ssl, time
from os.path import expanduser
from multiprocessing import Process, Event, Queue

from com_manager import Commanager
from parser import Parser
from utils import RETRY_DELAY, RETRY_TIMES, MULTI, COMMANDS_DIR

class IRC:
    def __init__(self, host, port, nick, channels, database, prefix, password, ssl):
        self.host = IRC.check_host(host)
        self.port = IRC.check_port(port)
        self.nick = IRC.check_nick(nick)
        self.channels = IRC.check_channels(channels)
        self.database = IRC.check_database(database)
        self.prefix = IRC.check_prefix(prefix)
        self.password = IRC.check_password(password)
        self.ssl = IRC.check_ssl(ssl)

        # load commands
        self.command_manager = Commanager(COMMANDS_DIR)

        # create database
        

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

            print("Retrying in {}s...".format(RETRY_DELAY * (retry_n + 1)))
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


    def ping(ircsock, arg):
        print("Pong!")
        ircsock.send(bytes("PONG :{}\n".format(arg), "UTF-8")) 


    def kicked(ircsock, arg):
        print("Kicked!")


    ################################### multi process ##########################################
    ############################################################################################

    def start_multi(self, ircsock):
        """ Start main bot function [obtain msg, store command] / [execute command, send output back] that supports multiprocess """      
        
        msg_queue = Queue()
        queue_event = Event()

        producer = Process(target=self.listening, args=(ircsock, queue_event, msg_queue,))
        consumer = Process(target=self.answering, args=(ircsock, queue_event, msg_queue,))

        producer.start()
        consumer.start()
        producer.join()
        consumer.join()


    def listening(self, ircsock, queue_event, queue):
        """ Obtain msg, queue command """

        # get msg
        for msg in self.get_msg(ircsock):
            print(">", msg)

            sender, receiver, command, args = Parser.parse_msg(msg)

            try:
                command = self.command_manager(command, args, sender, receiver)

            except NotPrivMsg:
                # if commands are not PRIVMSG handle them right away
                if command == 'PING':
                    IRC.ping(ircsock, args)

                elif command == 'KICK':
                    IRC.kicked(ircsock, args)

            else:
                # if not a command check next msg
                if not command: continue

                if queue.full(): queue_event.wait()
                queue.put(command)
                # unlock answering process
                queue_event.set()
        

    def answering(self, ircsock, queue_event, queue):
        """ Get command, execute it, and send back the output """

        # if queue empty wait for producer to add commands
        if queue.empty(): queue_event.wait()

        # get command from queue
        command = queue.get()

        # execute command
        self.send(command.execute())

        # unlock listening process if locked (can happen if queue is full)
        queue_event.set()
            

    ############################################################################################
    ############################################################################################


    ################################### single process #########################################
    ############################################################################################

    def start_single(self, ircsock):
        return True

    
    def get_msg(self, ircsock):
        line_buffer = str()

        while True:
            try:
                readbuffer = ircsock.recv(1024).decode('utf-8')
                head, *mid, tail = readbuffer.split('\n') 

                yield line_buffer + head

                line_buffer = str()

                for msg in mid:
                    yield msg

                line_buffer = line_buffer + tail

            except ValueError:
                line_buffer = line_buffer + readbuffer
                           
            
    def get_com(self, msg):
        sender, receiver, command, args = Parser.parse_msg(msg)

        try:
            return self.command_manager.mkcom(command, args, sender, receiver)

        except:
            return None
         
         

    ############################################################################################
    ############################################################################################


    ################################# atribute checking ########################################
    ############################################################################################

    #
    # TODO or not TODO
    #

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
