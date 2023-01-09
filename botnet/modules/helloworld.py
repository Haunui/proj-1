from botnet import logger
from botnet.modules.base_module import BaseModule

class Helloworld(BaseModule):
    def __init__(self, params):
        super().__init__(params)

    def exec(self):
        logger.success("Hello world !")
