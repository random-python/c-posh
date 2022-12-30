# _verbose.py

# Submodule of the posh package, defining classes for verbose output

__all__ = ["PIDWriter", "VerboseHeap", "VerboseSynch"]

from sys import stdout as _stdout
from os import getpid as _getpid
import _core


class PIDWriter(object):
    def __init__(self, output):
        self.output = output
        self.buf = ""

    def write(self, s):
        lines = (self.buf+s).split('\n')
        if lines:
            self.buf = lines[-1]
        else:
            self.buf = ""
        for line in lines[:-1]:
            self.output.write("[%s] %s\n" % (_getpid(), line.strip()))


class VerboseHeap(object):
    def __init__(self, name, heap, output=None):
        object.__init__(self)
        self.name = name
        self.heap = heap
        self.output = output or PIDWriter(_stdout)

    def alloc(self, size):
        self.output.write("%s: Allocating %d bytes" % (self.name, size))
        addr, size = self.heap.alloc(size)
        self.output.write(" at address %s (size %d).\n" % (addr, size))
        return addr, size

    def free(self, addr):
        self.output.write("%s: Freeing memory at address %s.\n" \
                          % (self.name, addr))
        return self.heap.free(addr)

    def realloc(self, addr, size):
        self.output.write("%s: Reallocating %d bytes from address %s" \
                          % (self.name, size, addr))
        addr, size = self.heap.realloc(addr, size)
        self.output.write("to %s (size %d).\n" % (addr, size))
        return addr, size


class VerboseSynch(object):
    def __init__(self, name, synch, output=None):
        object.__init__(self)
        self.name = name
        self.synch = synch
        self.output = output or PIDWriter(_stdout)

    def str(self, x):
        return "%s object at %s" % (type(x).__name__, _core.address_of(x))

    def enter(self, x, opname):
        self.output.write("%s: Entering %s on %s\n" \
                          % (self.name, opname, self.str(x)))
        if self.synch is None:
            rv = None
        else:
            rv = self.synch.enter(x, opname)
        return opname, rv

    def leave(self, x, opname_and_rv):
        opname, rv = opname_and_rv
        self.output.write("%s: Leaving %s on %s\n" \
                          % (self.name, opname, self.str(x)))
        if self.synch is not None:
            self.synch.leave(x, rv)

