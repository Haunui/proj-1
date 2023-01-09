import time
import importlib

from threading import Thread
from botnet import logger

TASK_WAITING=0
TASK_IN_PROGRESS=1
TASK_FINISH=2

class TaskManager(Thread):
    def __init__(self, module_manager):
        self.module_manager = module_manager
        self.tasks = {}
        self.status = True

        Thread.__init__(self)
        Thread.start(self)

    def stop(self):
        self.status = False

    def run(self):
        while self.status:
            try:
                l = list(self.tasks.items())
                task_id = l[0][0]
                task = l[0][1]
                if task.status == TASK_WAITING:
                    task.start()
                elif task.status == TASK_FINISH:
                    self.tasks.pop(task_id)
            except IndexError as e:
                pass

            time.sleep(1)

    def queue(self, topic, command):
        if topic == "botnet/task":
            e = command.split(":",2)

            task_id = e[0]

            if task_id not in self.tasks:
                task_action = e[1]
                
                try:
                    task_action_params = e[2]
                except:
                    task_action_params = ""

                try:
                    module = self.module_manager.MODULES[task_action]
                    module.manager = self.module_manager
                    self.tasks[task_id] = Task(module, task_action_params)

                    logger.debug("Task {} added".format(task_action))
                except:
                    logger.error("Module {} not found".format(task_action))

            else:
                logger.error("Task id already exists")


class Task():
    def __init__(self, module, params):
        self.module = module
        self.classname = self.module.__name__.split(".")[2].capitalize()
        self.params = params
        self.status = TASK_WAITING

    def start(self):
        self.status = TASK_IN_PROGRESS
        logger.info("Task {} started".format(self.classname))

        c = getattr(self.module, self.classname)
        self.instance = c(self.params.split(":"))
        self.instance.setFinishFunc(self.finish)
        self.instance.start()

    def finish(self, options=[]):
        self.status = TASK_FINISH

        if "reload_modules" in options:
            self.module.manager.load()
            logger.debug("Modules reloaded")
            self.module.manager.list()

        logger.info("Task {} done".format(self.classname))
