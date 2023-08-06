# TRIPLE - three letter modules
#
#

"default values"

__copyright__ = "Public Domain"

from .obj import Object

class Default(Object):

    "uses default values"

    def __getattr__(self, k):
        try:
            return super().__getattribute__(k)
        except AttributeError:
            return super().__getitem__(k, "")

