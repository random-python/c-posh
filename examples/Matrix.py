import sys, random, time
from pprint import pprint
from getopt import getopt
import thread
from threading import Semaphore
import posh

def matrix(N, M):
    """Creates a NxM matrix of only zeroes."""
    # The nslist is used since implicit synchronization is unneeded
    # for shared matrices in this application.
    return posh.nslist([posh.nslist([0]*M) for row in range(N)])

def random_matrix(N, M, min, max):
    """Creates a NxM matrix of random elements from range(min, max)."""
    m = matrix(N, M)
    for row in range(N):
        for col in range(M):
            m[row][col] = random.random() * (max-min) + min
    return m

def rows(m):
    """Returns the number of rows in a matrix."""
    return len(m)

def columns(m):
    """Returns the number of columns in a matrix."""
    return len(m[0])

def work(A, B, C, W, OnExit=None):
    """Worker no. W in the calculation A = B x C.
    Calculates every WORKERS row in A, starting at row W.
    """
    for row in range(W, rows(A), WORKERS):
        if not SILENT:
            print "Worker %d calculating row %d..." % (W, row)
        r = []
        for col in range(columns(A)):
            # Calculate A[row][col] by doing a dot product of
            # B's row and C's column
            sum = 0
            for x in range(columns(B)):
                sum += B[row][x] * C[x][col]
            r.append(sum)
        A[row] = r
    if OnExit:
        OnExit(W)
    return 0 # Exit status

def posh_version(B, C, WORKERS):
    A = matrix(rows(B), columns(C))
    A = posh.share(A)
    # Start all worker processes
    for W in range(WORKERS-1):
        posh.forkcall(work, A, B, C, W)
    # Run the last worker in this process
    work(A, B, C, WORKERS-1)
    # Wait for all workers to finish
    posh.waitall()
    return A

def threaded_version(B, C, WORKERS):
    A = matrix(rows(B), columns(C))
    done = Semaphore(0)
    def OnExit(W):
        done.release()
    # Start all worker threads
    for W in range(WORKERS-1):
        thread.start_new_thread(work, (A, B, C, W, OnExit))
    # Run the last worker in this thread
    work(A, B, C, WORKERS-1)
    # Wait for all workers to finish
    for W in range(WORKERS-1):
        done.acquire()
    return A

USAGE = """This program computes a matrix multiplication A = B x C
in parallell, using either processes or threads.

Options:
-m <number> Specifies the number of rows in B.
-n <number> Specifies the number of columns in B.
-l <number> Specifies the minimum value of the elements in B and C.
-h <number> Specifies the maximum value of the elements in B and C.
-w <number> Specifies the number of parallell workers to employ.
-i <number> Changes the time-slice for threads using sys.setcheckinterval.
-p          Uses multiple processes for the calculation.
-t          Uses multiple threads for the calculation.
-b          Uses both multiple processes and threads for the calculation,
            comparing the results.
-s          Silent. Shows no output during the calculation.

The default options used are:
-m 10 -n 10 -l 10 -h 20 -w 4 -b
"""

def main(args):
    global WORKERS, SILENT

    # Parse command-line arguments
    try:
        opts, args = getopt(args, "ptbsm:n:l:h:w:i:")
    except:
        print USAGE
        return
    if args:
        print USAGE
        return
    opts = dict(opts)
    M = int(opts.get("-m", 10))
    N = int(opts.get("-n", 10))
    MIN = int(opts.get("-l", 10))
    MAX = int(opts.get("-h", 20))+1
    WORKERS = int(opts.get("-w", 4))
    SILENT = "-s" in opts
    PROCESSES = "-p" in opts or "-b" in opts
    THREADS = "-t" in opts or "-b" in opts
    if not PROCESSES and not THREADS:
        PROCESSES = THREADS = 1
    if "-i" in opts:
        sys.setcheckinterval(int(opts["-i"]))

    B = random_matrix(M, N, MIN, MAX)
    C = random_matrix(N, M, MIN, MAX)
    if not SILENT:
        print
        for m in "BC":
            print "Matrix %s:" % m
            pprint(eval(m))
            print

    for step, doit, func in (("Threads", THREADS, threaded_version),
                             ("Processes", PROCESSES, posh_version)):
        if doit:
            start = time.time()
            A = func(B, C, WORKERS)
            stop = time.time()

            if not SILENT:
                print
                print "Matrix A = B x C:"
                pprint(A)
                print
            print "%s: %.2f seconds" % (step, stop-start)


if __name__ == "__main__":
    main(sys.argv[1:])


