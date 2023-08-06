# TRIPLE - three letter modules
#
#

"console (csl)"

__copyright__ = "Public Domain"

import atexit, readline, threading

from .bus import bus
from .evt import Event
from .krn import get_kernel
from .obj import Object
from .tsk import start

#:
cmds = []
#:
resume = {}

class Console(Object):

    "console class"

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()
        bus.add(self)

    def announce(self, txt):
        "silence announcing"

    def direct(self, txt):
        "print txt"
        print(txt.rstrip())

    def input(self):
        "loop for input"
        k = get_kernel()
        while 1:
            try:
                event = self.poll()
            except EOFError:
                print("")
                continue
            if not event.txt:
                continue
            event.orig = repr(self)
            k.put(event)
            event.wait()

    def poll(self):
        "wait for input"
        e = Event()
        e.orig = repr(self)
        e.otxt = e.txt = input("> ")
        return e

    def say(self, channel, txt):
        "strip channel from output"
        self.direct(txt)

    def start(self):
        "start console"
        k = get_kernel()
        setcompleter(k.cmds)
        start(self.input)

def complete(text, state):
    "complete matches"
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def getcompleter():
    "return the completer"
    return readline.get_completer()

def setcompleter(commands):
    "set the completer"
    cmds.extend(commands)
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))
