from threading import Thread
import time

from botnet import logger

# BaseModule class
class BaseModule(Thread):
    def __init__(self, params):
        logger.debug("module " + self.__class__.__name__ + " loaded")
        self.params = params

        self.finish_func_options = []

    # This method allow the task to retrieve when the module finish
    def setFinishFunc(self, func):
        self.finish_func = func

    # Start module
    def start(self):
        Thread.__init__(self)
        Thread.start(self)

        logger.debug(self.__class__.__name__ + " : " + str(self.params))

    def run(self):
        self.exec()
        self.finish_func(options=self.finish_func_options)

    # All do code are stored here
    def exec(self):
        pass


class TimedModule(BaseModule):
    def __init__(self, params, delay):
        super().__init__(params)

        self.timer = self.Timer(self, delay)
        self.status = True

    # All do code are stored here
    def exec(self):
        while self.status:
            self.in_loop()

    # Loop code are stored here
    def in_loop(self):
        pass

    # Timer class to monitor the task
    class Timer(Thread):
        def __init__(self, target, delay):
            self.target = target
            self.delay = int(delay)
            self.cdelay = self.delay

            Thread.__init__(self)
            Thread.start(self)

        def run(self):
            while self.cdelay > 0:
                time.sleep(1)
                self.cdelay -= 1

            self.target.status = False
