#!/usr/bin/env python3
#
# An IRC bot.
#

from utils import *
import os, fcntl
import socket
import time
import threading

# TODO: general IRC msg class/type

class Ponger(threading.Thread):
    def run(self):
        logging.info("Ponger started")
        time.sleep(1)
        logging.info("Ponger ended")

class PipeInterface(threading.Thread):
    def __init__(self, roshanbot):
        threading.Thread.__init__(self)
        self.roshanbot = roshanbot
        self.pipe = "/home/raehik/test"

    def run(self):
        try:
            pipe_out = open(self.pipe, "r")
        except:
            logging.error("PipeInterface: couldn't open pipe")
        logging.info(pipe_out.read())
        #self.roshanbot.send(msg)
        # TODO 4 lines below
        # setup pipe
        self.cmd_pipe = "/home/raehik/test"
        self.cmd_pipe_out = open(self.cmd_pipe, "r")
        fcntl.fcntl(self.cmd_pipe_out, fcntl.F_SETFL, os.O_NONBLOCK)

class RoshanBot:
    ENC = "utf-8"
    SOCK_MAX_BYTES = 1024
    TIMEOUT_SECS = 10

    def __init__(self):
        logging.debug("roshanbot starting...")

        # config variables {{{
        self.nick = "roshan"
        self.username = "username-todo"
        self.realname = "roshanbot"

        self.srv_host = "localhost"
        self.srv_port = 6667
        #self.srv_host = "irc.cs.kent.ac.uk"
        #self.srv_port = 6697

        self.quit_msg = "Roshan has fallen to the Dire!"
        # }}}
        self.tmp_channel = "#bot-testing"

        self.srv_sock = socket.socket()
        self.readbuf = ""

        self.connect()

        # tmp
        self.send("JOIN {}".format(self.tmp_channel))
        self.send("PRIVMSG {} :Hello Master\r\n".format("raehik"))

    def connect(self):
        connected = False
        while not connected:
            logging.info("connecting to server...")
            try:
                self.srv_sock.connect((self.srv_host, self.srv_port))
                # TODO: optional PASS
                self.send("NICK :{}".format(self.nick))
                self.send("USER {} {} bla :{}".format("ident", "host", self.realname))
                connected = True
            except socket.error:
                logging.warning("connection failed, trying again in {} seconds...".format(RoshanBot.TIMEOUT_SECS))
                time.sleep(RoshanBot.TIMEOUT_SECS)

    def send(self, msg):
        """Encodes a string as UTF-8 and sends it to the socket."""
        logging.debug("> {}".format(msg))
        self.srv_sock.send(bytes("{}\n".format(msg).encode(RoshanBot.ENC)))

    def quit(self):
        self.send("QUIT :{}".format(self.quit_msg))

    def main_loop(self):
        i = 0
        while True:
            i += 1
            logging.debug("loop {}".format(i))
            logging.info(self.cmd_pipe_out.read())
            ################################
            # get bytes from the socket (will return fewer if fewer available)
            self.readbuf += self.srv_sock.recv(RoshanBot.SOCK_MAX_BYTES).decode(RoshanBot.ENC)

            # split messages on newlines
            msg = self.readbuf.split("\n")
            self.readbuf = msg.pop()

            logging.debug("< {}".format(msg))
            for parts in msg:
                #parts = str.rstrip(parts)
                parts = str.split(parts)

                if(parts[0] == "PING"):
                    rosh.send("PONG {}".format(parts[1]))
                if(parts[1] == "PRIVMSG"):
                    sender = ""
                    for char in parts[0]:
                        if(char == "!"):
                            break
                        if(char != ":"):
                            sender += char
                    size = len(parts)
                    i = 3
                    message = ""
                    while i < size:
                        message += parts[i] + " "
                        i = i + 1
                    message.lstrip(":")
                    rosh.send("PRIVMSG {} {}".format(sender, message))



if __name__ == "__main__":
    rosh = RoshanBot()
    try:
        rosh.main_loop()
    except KeyboardInterrupt:
        rosh.quit()
