# TRIPLE - three letter modules
#
#

"module loader (ldr)"

__copyright__ = "Public Domain"

import importlib

from .obj import Object

class Loader(Object):

    "holds modules table"

    #:
    table = Object()

    def load(self, name):
        "load module"
        if name not in self.table:
            self.table[name] = importlib.import_module(name)
        return self.table[name]
