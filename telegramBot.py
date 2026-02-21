
from telebot import TeleBot
from definitions import Telegram


class TelegramBot:
    """Summary of class here

    Attributes:
        instance (str): telegram instance
        lastCommand (str): last commmand saved
        entryData (str): category of the command where the user input will be saved

    Methods:
        initBot(): 
        inifinityPolling(): 
    """

    instance = None
    lastCommand = None
    entryData = None

    #---------------------------------------------------------------

    @classmethod
    def initBot(cls):
        """ -- """
        TelegramBot.instance = TeleBot(Telegram.BOT_TOKEN, disable_notification=True)

    #---------------------------------------------------------------

    @classmethod
    def inifinityPolling(cls):
        """ -- """
        if TelegramBot.instance is None:
            TelegramBot.initBot()

        TelegramBot.instance.remove_webhook()
        TelegramBot.instance.infinity_polling()

    #---------------------------------------------------------------
