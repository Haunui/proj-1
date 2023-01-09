import os
from importlib import import_module

from botnet import logger

# Modules paths (botnet/modules)
MODULES_PATH="botnet.modules"

# ModuleManager class
class ModuleManager():
    def __init__(self):
        self.MODULES={}

    # Load modules
    def load(self):
        self.MODULES={}
        for path in os.listdir(MODULES_PATH.replace(".","/")):
            if path.endswith('.py') and path.replace('.py', '') not in ['base_module', 'timed_module']:
                filename = path.replace(".py","")
                self.MODULES[filename] = import_module(MODULES_PATH + "." + filename)

    # List modules
    def list(self):
        s=""
        for k in self.MODULES.keys():
            s+=k + ", "

        logger.info("Liste des modules : " + s[:-2])
