# TRIPLE - three letter modules
#
#

"database (dbs)"

__copyright__ = "Public Domain"


from triple import obj

from .obj import hook, update, os
from .ofn import format, search
from .tms import fntime
from .utl import get_type

def all(otype, selector=None, index=None, timed=None):
    "return all matching objects"
    nr = -1
    if selector is None:
        selector = {}
    for fn in fns(otype, timed):
        o = hook(fn)
        if selector and not search(o, selector):
            continue
        if "_deleted" in o and o._deleted:
            continue
        nr += 1
        if index is not None and nr != index:
            continue
        yield fn, o

def deleted(otype):
    "return all deleted objects"
    for fn in fns(otype):
        o = hook(fn)
        if "_deleted" not in o or not o._deleted:
            continue
        yield fn, o

def every(selector=None, index=None, timed=None):
    "return subset from all objects"
    nr = -1
    if selector is None:
        selector = {}
    for otype in os.listdir(os.path.join(obj.wd, "store")):
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not search(o, selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

def find(otype, selector=None, index=None, timed=None):
    "find objects"
    nr = -1
    if selector is None:
        selector = {}
    for fn in fns(otype, timed):
        o = hook(fn)
        if selector and not search(o, selector):
            continue
        if "_deleted" in o and o._deleted:
            continue
        nr += 1
        if index is not None and nr != index:
            continue
        o.__type__ = otype
        yield fn, o

def find_event(e):
    "find objects based on event"
    nr = -1
    for fn in fns(e.otype, e.timed):
        o = hook(fn)
        if e.gets and not search(o, e.gets):
            continue
        if "_deleted" in o and o._deleted:
            continue
        nr += 1
        if e.index is not None and nr != e.index:
            continue
        yield fn, o

def last(o):
    "return last object"
    path, l = lastfn(str(get_type(o)))
    if  l:
        update(o, l)

def lastmatch(otype, selector=None, index=None, timed=None):
    for fn, o in find(otype, selector, index, timed):
        yield fn, o
        break

def lasttype(otype):
    "return last object of type"
    fnn = fns(otype)
    if fnn:
        return hook(fnn[-1])

def lastfn(otype):
    "return filename of last object"
    fn = fns(otype)
    if fn:
        fnn = fn[-1]
        return (fnn, hook(fnn))
    return (None, None)

def fns(name, timed=None):
    "return filenames"
    if not name:
        return []
    p = os.path.join(obj.wd, "store", name) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if timed and "from" in timed and timed["from"] and fntime(p) < timed["from"]:
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)
