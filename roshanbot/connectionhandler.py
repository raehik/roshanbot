#
# Handles socket connection to the IRC server.
#

from utils import *
import socket
import threading
import time

class ConnectionHandler:
    # Encoding to use for encoding all sent messages and decoding all
    # received messages.
    # TODO: possibility to decode other encodings? Shift-JIS, UTF-16 main ones
    ENC = "utf-8"

    # Maximum amount of bytes to read from the socket each time.
    # TODO: why? and what? lmao
    SOCK_MAX_BYTES = 1024

    # How long to wait while attempting to connect the socket.
    TIMEOUT_SECS = 10

    # Message separator.
    # Defined as CR+LF (\r\n) in RFC 1459.
    MSG_SEP = "\r\n"

    def __init__(self, host, port, nick, username, realname):
        self.host = host
        self.port = port
        self.nick = nick
        self.username = username
        self.realname = realname

        # TODO: another thread which waits for 001 through 004 (or just 001, or
        #       just 004), which sets this true
        #       according to RFC 2813 section 5.2.1, the server is required to
        #       send all 4 messages
        self.is_registered = False

        self.quit_msg = "Roshan has fallen to the Dire!" # TODO

        self.sock = socket.socket()

    def send(self, msg, needs_reg=True):
        """Encodes a string as UTF-8 and sends it to the socket."""
        if needs_reg and not self.is_registered:
            logging.debug("message needs registered but we aren't yet")
            return
        logging.debug("> {}".format(msg))
        self.sock.send(bytes(
            "{}{}".format(msg, ConnectionHandler.MSG_SEP).encode(
                ConnectionHandler.ENC)))

    def tmp_cmds(self):
        # TODO: temporary on-start commands
        logging.error("cheating, I set is_registered")
        self.is_registered = True
        self.send("JOIN #test")
        self.send("PRIVMSG raehik :sup nigga")

    def register(self):
        """Register with the server."""
        logging.info("registering...")
        # TODO: optional PASS
        self.send("NICK :{}".format(self.nick),
                needs_reg=False)
        time.sleep(1)
        self.send("USER {} {} bla :{}".format("ident", "host", self.realname),
                needs_reg=False)
        self.tmp_cmds()

    def connect(self):
        """Try to make a connection to the server."""
        logging.info("connecting to server...")

        # Set timeout.
        # Note that we use a thread for the socket, so we use a blocking
        # connection (as is the default) -- we'll set this back to 0 when we're
        # connected.
        self.sock.settimeout(ConnectionHandler.TIMEOUT_SECS)

        connected = False
        while not connected:
            try:
                self.sock.connect((self.host, self.port))
                connected = True
            # exception catches {{{
            except socket.timeout as e:
                logging.error("timed out while trying to connect: {}:{}".format(self.host, self.port))
                self.close()
                sys.exit(10) # TODO: exit codes? who really cares but still
            except socket.gaierror as e:
                logging.error("error resolving host: {}".format(self.host))
                self.close()
                sys.exit(11)
            except Exception as e:
                logging.error("unknown error connecting socket: {}:{}".format(self.host, self.port))
                raise e
            # }}}

        # connection successful: make the socket blocking again
        self.sock.settimeout(None)

        # start the socket reading thread
        t = threading.Thread(target=self.read_sock)
        t.start()

    def close(self):
        """Close the socket connection safely.

        Note that this does not close the IRC connection 'nicely' -- that
        should be done elsewhere.
        """
        logging.info("closing connection...")
        self.sock.close()

    def read_sock(self):
        # buffer to hold incomplete messages (needs to persist between loops)
        readbuf = ""

        while True:
            # get bytes from the socket (will return fewer if fewer available)
            readbuf += self.sock.recv(ConnectionHandler.SOCK_MAX_BYTES).decode(ConnectionHandler.ENC)

            # split messages on specified separator
            msgs = readbuf.split(ConnectionHandler.MSG_SEP)
            readbuf = msgs.pop()

            for m in msgs:
                logging.debug("< {}".format(m))
                #parts = str.rstrip(parts)
                parts = str.split(m)

                if(parts[0] == "PING"):
                    self.send("PONG {}".format(parts[1]),
                            needs_reg=False)
                if(parts[1] == "PRIVMSG"):
                    sender = ""
                    for char in parts[0]:
                        if(char == "!"):
                            break
                        if(char != ":"):
                            sender += char
                    self.send("PRIVMSG {} :u said summin bout me???".format(sender))


if __name__ == "__main__":
    logging.error("This class cannot be run directly.")
    sys.exit(1)
