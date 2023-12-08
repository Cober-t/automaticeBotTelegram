
from telebot import TeleBot
from definitions import Telegram


class TelegramBot:

    instance = None

    @classmethod
    def initBot(cls):
        TelegramBot.instance = TeleBot(Telegram.BOT_TOKEN, disable_notification=True)


    @classmethod
    def inifinityPolling(cls):
        if TelegramBot.instance is None:
            TelegramBot.initBot()
        TelegramBot.instance.infinity_polling()
