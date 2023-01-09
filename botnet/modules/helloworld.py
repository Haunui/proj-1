from botnet import logger
from botnet.modules.base_module import BaseModule

# Helloworld class
class Helloworld(BaseModule):
    def __init__(self, params):
        super().__init__(params)

    # Display "hello world !"
    def exec(self):
        logger.success("Hello world !")
