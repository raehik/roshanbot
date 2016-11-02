Start-up
--------

  1. THREAD: UNTIL TRUE: connect & register ([PASS, ]NICK, USER)
  2. THREAD: start ponger
  3. THREAD: open named pipe for reading

### 1: connect
yeah

### 2: ponger
yeah

### 3: open named pipe
Doesn't matter yet, just start a thread which feeds fake info


Types of plugin
---------------

roshanbot should be as modular as possible. So for every message or command sent
to/received by it, roshanbot needs to know how to know whether it can respond to
it. For this, each plugin must tell roshanbot its **capabilities**:

  1. **Command:** *keyword -> msg*  
     responds to certain keywords
  2. **Filter:**  *msg -> operation -> msg*  
     transforms a string in some way

Some operations must be outside plugins:

  1. Stream operations (en/decoding)
  2. Command detection: prefix, highlights, privmsg etc.
  3. 


Types
-----

### msg

Holds a message waiting to be sent. This includes:

  * message string
  * channel/user
  * , plus information about certain formatting things which shouldn't
be changed


Command detection
-----------------

The bot should *always* know how it is being talked to. Some commands may only
exist in certain input methods.

### Prefix
Probably want '!'. Should be easy to change though.

### Pre-highlights
*Must be at start (otherwise cmd could be hard to parse).* Probably treat the
same as prefix.

### Pre-pseudo-highlights
*Same as above.* Make some nicknames for roshanbot that are treated the same as
his actual nick.  Also potentially some fake nicks (e.g. "dota: item random" ->
dota) for speedier commands.

Quite unsure about this one. Probably better ways to implement it: like just use
prefix. Or multiple prefixes?

### Private message
Don't need prefix in this case.


Functions
---------

### RPS with privmsg cheating
So you can mess people up xD

### MUD / text adventure game
Would be cool.

### Dota voice responses
And aliases for them e.g. if it ever reads 'waifu', give cute CM response.
Should include link & quote, or just link. Use reddit account GitHub (TODO:
find).

### Dota items
Random or item name, give info.

### Hyperlinks
Just pretend to override Marvin or sth.
