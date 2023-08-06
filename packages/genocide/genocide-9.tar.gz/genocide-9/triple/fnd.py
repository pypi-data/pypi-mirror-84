# TRIPLE - 3 letter modules
#
#

"find objects (fnd)"

__copyright__ = "Public Domain"

import os, time

from triple import obj
from .dbs import find
from .tms import elapsed, fntime
from .krn import get_kernel
from .obj import get, keys
from .ofn import format
from .utl import cdir

def fnd(event):
    "locate and show objects on disk"
    if not event.args:
        assert obj.wd
        wd = os.path.join(obj.wd, "store", "")
        cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0].split(".")[-1].lower() for x in fns})
        if fns:
            event.reply(",".join(fns))
        return
    nr = -1
    args = []
    try:
        args = event.args[1:]
    except IndexError:
        pass
    k = get_kernel()
    types = get(k.names, event.args[0], [event.cmd,])
    for otype in types:
        for fn, o in find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            pure = True
            if not args:
                args = keys(o)
            if "f" in event.prs.opts:
                pure = False
            txt = "%s %s" % (str(nr), format(o, args, pure, event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)
