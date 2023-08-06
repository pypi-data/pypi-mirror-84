# TRIPLE - three letter modules
#
#

"event (evt)"

__copyright__ = "Public Domain"

import threading

from .bus import bus
from .dft import Default
from .obj import Object, update
from .prs import parse

class Event(Object):

    "event class"

    __slots__ = ("prs", )

    def __init__(self):
        super().__init__()
        self.args = []
        self.cmd = ""
        self.channel = ""
        self.orig = ""
        self.otxt = ""
        self.prs = Default()
        self.ready = threading.Event()
        self.rest = ""
        self.result = []
        self.thrs = []
        self.txt = ""

    def direct(self, txt):
        "send txt via bus"
        bus.say(self.orig, self.channel, txt)

    def parse(self):
        "parse an event"
        o = Default()
        parse(o, self.otxt)
        update(self.prs, o)
        args = self.prs.txt.split()
        if args:
            self.cmd = args.pop(0)
        if args:
            self.args = args
            self.rest = " ".join(args)

    def reply(self, txt):
        "add txt to result"
        self.result.append(txt)

    def show(self):
        "display result"
        for txt in self.result:
            self.direct(txt)

    def wait(self):
        "wait for event to finish"
        self.ready.wait()
        res = []
        for thr in self.thrs:
            res.append(thr.join())
        return res
