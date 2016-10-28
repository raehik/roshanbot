#!/usr/bin/env python3
#
# An IRC bot.
#

from utils import *
import socket

class RoshanBot:
    def __init__(self):
        logging.debug("roshanbot starting...")

        self.nick = "roshan"
        self.username = "username-todo"
        self.realname = "roshanbot"

        self.srv_host = "irc.cs.kent.ac.uk"
        self.srv_port = 6697
        self.srv_sock = socket.socket()

        self.tmp_channel = "#irc-sandbox"

        self.connect()

    def connect(self):
        self.srv_sock.send(bytes("hi"))

if __name__ == "__main__":
    rosh = RoshanBot()
