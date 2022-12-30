import posh
from random import randrange, seed
import time

class Queue(object):
    """Silly, inefficient queue class."""
    def __init__(self, copy=None):
        print "Initializing %s object" % type(self).__name__
        if copy is None:
            self.items = ()
        else:
            self.items = tuple(copy.items)

    def get(self):
        i = self.items[0]
        self.items = self.items[1:]
        return i
    
    def put(self, value):
        self.items += (value,)

    def empty(self):
        return not len(self.items)

    def size(self):
        return len(self.items)

class Producer(object):
    def __init__(self, name, queue):
        self.name = name
        self.queue = queue
        self.itemno = 0
        self.quit = 0

    def run(self):
        """Produce items until the end of time."""
        name = "%s [%s]" % (self.name, posh.getpid())
        seed(posh.getpid())
        try:
            while 1:
                time.sleep(randrange(10)/10.0)
                item = self.newitem()
                print "Producer %s produced item: %s" % (name, item)
                self.queue.put(item)
        except KeyboardInterrupt:
            print "Producer %s exiting." % name
            return 0 # Exit status
        except:
            import traceback
            traceback.print_exc()
            print "Producer %s exiting due to uncaught exception." % name
            return 1 # Exit status

    def newitem(self):
        """Creates a random item."""
        self.itemno += 1
        return self.itemno
    

class Consumer(object):
    def __init__(self, name, queue):
        self.name = name
        self.queue = queue

    def run(self):
        """Consume items until the end of time."""
        name = "%s [%s]" % (self.name, posh.getpid())
        seed(posh.getpid())
        try:
            while 1:
                try:
                    item = self.queue.get()
                    print "Consumer %s consumed item: %s" % (name, item)
                except IndexError:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print "Consumer %s exiting." % name
            return 0 # Exit status
        except:
            import traceback
            traceback.print_exc()
            print "Consumer %s exiting due to uncaught exception." % name
            return 1 # Exit status
            

def testqueue(q):
    print "Testing %s" % type(q).__name__
    assert q.empty()
    q.put("test")
    test = q.get()
    assert test == "test"
    assert q.empty()


if __name__=="__main__":
     posh.allow_sharing(Queue)
     q = Queue()
     testqueue(q)
     q = posh.share(q)
     testqueue(q)

     # Create all producers/consumers
     pcs = []
     pcs.append(Producer("p1", q))
     pcs.append(Consumer("c1", q))
     pcs.append(Consumer("c2", q))

     # Start all producers/consumers
     for pc in pcs:
         posh.forkcall(pc.run)

     # Print status information until interrupted
     try:
         while 1:
             print "Queue size:", q.size()
             time.sleep(1)
     except KeyboardInterrupt:
         pass

     # Wait for all of the producers/consumers to terminate
     while 1:
         try:
             posh.waitall()
         except KeyboardInterrupt:
             pass
     print "All processes terminated."

        


    

    
