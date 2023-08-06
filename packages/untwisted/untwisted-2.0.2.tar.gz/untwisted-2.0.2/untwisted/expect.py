from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from queue import Queue, Empty
from untwisted.dispatcher import Dispatcher
from untwisted import core
from untwisted.event import LOAD, CLOSE
from untwisted.waker import waker

class Expect(Thread, Dispatcher):
    """
    This class is used to spawn processes.

    python = Expect('python2.7', '-i')
    python.send('print "hello world"')
    python.terminate()
    python.destroy()
    """

    SIZE = 1024 * 124

    def __init__(self, *args, **kwargs):
        """
        """

        self.child = Popen(args, stdout=PIPE, stdin=PIPE,  
        stderr=STDOUT, **kwargs)

        self.stdin     = self.child.stdin
        self.stdout    = self.child.stdout
        self.stderr    = self.child.stderr
        self.args      = args
        self.queue     = Queue()
        self.terminate = self.child.terminate
        core.gear.pool.append(self)

        Dispatcher.__init__(self)
        Thread.__init__(self)

        self.start()

    def send(self, data):
        """
        Send data to the child process through.
        """
        self.stdin.write(data)
        self.stdin.flush()

    def run(self):
        """
        """

        while True:
            data = self.feed()
            waker.wake_up()
            if not data: 
                break

        self.child.wait()

    def feed(self):
        try:
            data = self.stdout.readline()
        except Exception as e:
            data = ''
        finally:
            self.queue.put_nowait(data)
            return data

    def update(self):
        """
        """
        while not self.queue.empty():
            self.dispatch()

    def dispatch(self):
        data = self.queue.get_nowait()
        if not data: 
            self.drive(CLOSE)
        else: 
            self.drive(LOAD, data)

    def destroy(self):
        """
        Unregister up from untwisted reactor. It is needed
        to call self.terminate() first to kill the process.
        """
        core.gear.pool.remove(self)    
        self.base.clear()








