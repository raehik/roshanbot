#!/usr/bin/env python3
#
# An IRC bot.
#

from utils import *
import connectionhandler
import threading
import os
import fcntl
import sys

class Ponger(threading.Thread):
    def __init__(self, roshanbot):
        self.roshanbot = roshanbot

    def run(self):
        logging.info("Ponger started")

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
    """Main bot class."""

    def __init__(self):
        logging.debug("roshanbot starting...")
        self.connection = connectionhandler.ConnectionHandler("localhost", 6667, "roshan", "username", "realname")
        #host = "irc.cs.kent.ac.uk"
        #port = 6697

    def start(self):
        """Start the bot."""
        self.connection.connect()
        self.connection.register()

    def stop(self):
        """Stop the bot."""
        # IRC QUIT
        self.connection.send("QUIT :{}".format(self.quit_msg), needs_reg=False)

        # close socket
        self.connection.close()



if __name__ == "__main__":
    rosh = RoshanBot()
    try:
        rosh.start()
    except KeyboardInterrupt:
        logging.info("keyboard interrupt detected, stopping...")
        rosh.stop()
