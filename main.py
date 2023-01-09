from botnet.module_manager import ModuleManager
from botnet.bot.bot import RegisteredBot, GuestBot

def main1():
    bot = RegisteredBot("client123", "localhost")
    bot.connect()
    bot.subscribe("botnet/task")
    bot.listen()

def main():
    bot = GuestBot("localhost")

    client_id = bot.getID()

    if client_id == None:
        bot.connect()
        bot.listen()
    else:
        bot.toRegisteredBot(client_id)


if __name__ == "__main__":
    main1()
