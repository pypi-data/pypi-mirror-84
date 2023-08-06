# TRIPLE - three letter modules
#
#

"tasks (tsk)"

__copyright__ = "Public Domain"

import queue, threading, time

from .obj import Object
from .utl import get_exception, get_name

class Task(threading.Thread):

    "task class"

    def __init__(self, func, *args, name="noname", daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._name = name
        self._result = None
        self._queue = queue.Queue()
        self._queue.put((func, args))
        self.sleep = 0
        self.state = Object()

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def run(self):
        "run a task"
        func, args = self._queue.get()
        self.setName(self._name)
        try:
            self._result = func(*args)
        except Exception as ex:
            print(get_exception())
        
    def wait(self, timeout=None):
        "wait for task to finish"
        super().join(timeout)
        return self._result

def start(func, *args, **kwargs):
    "start a task"
    name = kwargs.get("name", get_name(func))
    t = Task(func, *args, name=name, daemon=True)
    t.start()
    return t
