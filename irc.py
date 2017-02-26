import sys, socket, ssl, time, os, select, datetime
from threading import Thread, Event, Lock
from queue import Queue

from com_manager import Commanager
from parser import Parser
from database_manager import DBM
from utils import RETRY_DELAY, RETRY_TIMES, MULTI, COMMANDS_DIR, SCHEMA, TIMEOUT, GOODBYE
from timevent import Timevent

import ircerror
import commanderror

class IRC:
    """ Class that do most of the irc work """

    def __init__(self, host, port, nick, channels, database, prefix, password, ssl):
        self.host = IRC.check_host(host)
        self.port = IRC.check_port(port)
        self.nick = IRC.check_nick(nick)
        self.channels = IRC.check_channels(channels)
        self.prefix = IRC.check_prefix(prefix)
        self.password = IRC.check_password(password)
        self.ssl = IRC.check_ssl(ssl)

        # load commands
        print("Loading commands...")
        self.command_manager = Commanager(COMMANDS_DIR)
        print(self.command_manager.commands)
        print("...done!")

        # create database
        try:
            self.database = DBM(database, SCHEMA)
        except:
            raise

        # time events
        self.time_event = {"ping": Timevent(True, 0.0, TIMEOUT, self.command_manager.mkcom("reset", None, None, None, None))}


    def connect(self):
        """ Main connection structure. Socket generation and checking on connection status """

        retry_n = 0
        while retry_n <= RETRY_TIMES:
            try:
                ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ircsock.connect((self.host, self.port))

                if self.ssl:
                    # secure connection
                    ircsock = ssl.wrap_socket(ircsock)

                self.server_login(ircsock)

                if MULTI:
                    # multiprocess ramenbot
                    self.start_multi(ircsock)
                else:
                    # single process ramenbot
                    self.start_single(ircsock)

                retry_n = 0

            except ConnectionRefusedError as e:
                print(e)#, file=sys.stderr)
                pass
            except socket.gaierror as e:
                print(e)
                pass

            print("Retrying in {}s...".format(RETRY_DELAY * (retry_n + 1), file=sys.stderr))
            retry_n+=1
            time.sleep(RETRY_DELAY * (retry_n))


    def server_login(self, ircsock):
        """ Connects to the irc server and if you set up a password it logs to NickServ """

        ircsock.send(bytes("NICK {}\r\n".format(self.nick), "UTF-8"))
        time.sleep(.5)
        ircsock.send(bytes("USER {} {} {} :ramenbot\r\n".format(self.nick, self.nick, self.nick), "UTF-8"))
        time.sleep(.5)

        if self.password:
            # here goes nickserv login #
            print("pass")
            

    def chan_join(self, ircsock):
        print("Joining Chans...")
        for chan in self.channels: ircsock.send(bytes("JOIN {}\r\n".format(chan), "UTF-8"))


    def ping(ircsock, arg):
        print("Pong! [{}]".format(datetime.datetime.now()))
        ircsock.send(bytes("PONG :{}\r\n".format(arg), "UTF-8")) 


    def kicked(ircsock, arg):
        print("Kicked!")


    ################################### multi process ##########################################
    ############################################################################################

    def start_multi(self, ircsock):
        """ Start main bot function [obtain msg, store command] / [execute command, send output back] that supports multiprocess """      

        msg_queue = Queue()
        msg_queue_event = Event()
        timer_queue = Queue()
        timer_queue_event = Event()

        exit_event = Event()
        exit_event.set()

        producer = Thread(target=self.listening, args=(ircsock, exit_event, msg_queue_event, msg_queue,))
        consumer = Thread(target=self.answering, args=(ircsock, msg_queue_event, msg_queue, timer_queue, timer_queue_event))
        timer = Thread(target=self.timer, args=(msg_queue, msg_queue_event, timer_queue, timer_queue_event))

        try:
            producer.start()
            consumer.start()
            timer.start()
            producer.join()
            consumer.join()
            timer.join()

        except KeyboardInterrupt:
            exit_event.clear()
            raise


    def listening(self, ircsock, exit_event, msg_queue_event, msg_queue):
        """ Obtain msg, queue command """

        try:
            # get msg
            for msg in self.get_msg(ircsock, exit_event):
                if not msg: raise ircerror.IRCShutdown("Server closed connection")

                # parsing irc msg
                sender, receiver, irc_command, irc_args = Parser.parse_msg(msg)

                # if irc commands are not PRIVMSG handle them right away
                # and get next msg
                if irc_command != 'PRIVMSG':
                    if irc_command == 'PING':
                        IRC.ping(ircsock, irc_args)
                        self.super_queue(msg_queue, self.command_manager.mkcom("ping", [TIMEOUT], self.nick, "#test", self.database), msg_queue_event)
                    elif irc_command == 'KICK':
                        IRC.kicked(ircsock, irc_args)
                    elif irc_command == 'MODE':
                        self.chan_join(ircsock)

                    continue

                # triggers
                try:
                    self.super_queue(msg_queue, self.command_manager.mkcom("checkon", None, self.nick, receiver, self.database), msg_queue_event)

                except commanderror.NoCommandFound as e:
                    print("Trigger not working: {}".format(e.description), file=sys.stderr)
                    pass

                #except commanderror.CommandException as e:
                #    print("Trigger not working: {}".format(e.description), file=sys.stderr)
                #    pass

                ####################
                # command handling #
                ####################

                # find and create command
                name, args = Parser.find_command(irc_args, self.prefix)

                try:
                    self.super_queue(msg_queue, self.command_manager.mkcom(name, args, sender, receiver, self.database), msg_queue_event)

                except commanderror.NoCommandFound:
                    pass

                #except commanderror.CommandException:
                #    print("The command is not working properly", file=sys.stderr)
                #    pass
                
        except ircerror.IRCShutdown as e:
            print(e.description, file=sys.stderr)

        except OSError as e:
            # horrible hack to end listening thread life
            # fix someday
            print("File descriptor error, probably from disconnection exception", file=sys.stderr)
            pass

        except KeyboardInterrupt:
            pass

        finally:
            print("Closing listening thread")
            if msg_queue.full(): msg_queue_event.wait()
            msg_queue.put(None)
            msg_queue_event.set()


    def answering(self, ircsock, msg_queue_event, msg_queue, timer_queue, timer_queue_event):
        """ Get command, execute it, and send back the output """

        try:
            while True:
                # if queue empty wait for producer to add commands
                if msg_queue.empty(): msg_queue_event.wait()

                # get command from queue
                command = msg_queue.get()

                # if command is none, then listening process closed
                # and we need to close this process as well
                # if command is "reset" timer wants ramenbot to
                # reset the connection with the server
                if command == None: break
                elif command == "reset": raise ConnectionRefusedError

                try:
                    # execute command and send command/event
                    self.send(command.execute(), ircsock, timer_queue, timer_queue_event)

                except commanderror.CommandException:
                    print("A command is not working properly, debug it!", file=sys.stderr)


        except KeyboardInterrupt:
            pass

        finally:
            timer_queue.put(None)
            timer_queue_event.set()
            print("Closing answering thread")
            ircsock.send(bytes("QUIT {}\n\r".format(GOODBYE), "UTF-8"))
            ircsock.shutdown(socket.SHUT_RDWR)
            ircsock.close()
        

    def timer(self, msg_queue, msg_queue_event, timer_queue, timer_queue_event):
        """ Checks time and trigger events """
        
        try:
            last = time.monotonic()
            while True:

                # check & update events
                time.sleep(.5)
                now = time.monotonic()

                try:
                    for _,tv in self.time_event.items():
                        tv.update(abs(now - last))

                        if tv.is_time():
                            ###################################
                            # timer shouldn't execute commands
                            # that's the answering thread's job
                            # find workarround
                            ####################################
                            self.super_queue(msg_queue, tv.execute(), msg_queue_event)

                except commanderror.CommandException:
                    print("A command is no working properly, debug it!", file=sys.stderr)
                    pass

                last = now 


                if timer_queue.empty(): continue

                event = timer_queue.get()
                if not event: break

                print(event)

                # check for event change
                if event[0] == "reset":
                    self.time_event[event[1]].reset()
                elif event[0] == "disable":
                    self.time_event[event[1]].disable()
                elif event[0] == "enable":
                    self.time_event[event[1]].enable()
                    

        except KeyboardInterrupt:
            pass

        finally:
            # reset all events
            for _,tv in self.time_event.items(): tv.reset()
            print("Closing timer thread")



    ############################################################################################
    ############################################################################################


    ################################### single process #########################################
    ############################################################################################

    def start_single(self, ircsock):
        # this thing will never be done
        return True

    
    def get_msg(self, ircsock, exit_event):
        line_buffer = str()

        while True:
            # check if exit event is set and exit iterator if false
            if not exit_event.is_set(): return

            # check if socket ready to read
            ready_to_read, _, __, = select.select([ircsock], [], [], 0.1)
            # if not ready check again
            if not ready_to_read: continue

            readbuffer = ircsock.recv(1024).decode("UTF-8", "ignore")

            # if buffer is '', then connection was close
            if not readbuffer: yield readbuffer

            # this fixes msg if it gets truncated
            try:
                head, *mid, tail = readbuffer.split('\n') 
                yield line_buffer + head

                line_buffer = str()

                for msg in mid:
                    yield msg

                line_buffer = line_buffer + tail

            except ValueError:
                line_buffer = line_buffer + readbuffer
     

    def send(self, answer, ircsock, timer_queue=None, timer_queue_event=None):
        try:
            for msg in answer:
                try:
                    ircsock.send(bytes("PRIVMSG {}\n\r".format(msg["msg"]), "UTF-8"))
                except KeyError:
                    self.super_queue(timer_queue, msg["event"])
        
        except TypeError as err:
            print(err, file=sys.stderr)
            pass
            

    def super_queue(self, queue, data, event=None):
        # wait if queue is full
        if queue.full() and event: event.wait() 

        # put data in queue
        queue.put(data)

        # unlock answering process
        if event: event.set()


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
