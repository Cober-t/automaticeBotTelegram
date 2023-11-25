'''Main Utils class'''
import os
import json

from definitions import Telegram, NotionProterties
from checkGrammarText import CheckGrammar
from telegramBot import TelegramBot


class Utils:


    @classmethod
    def sendMessage(cls, message):

        TelegramBot.instance.send_message(Telegram.CHAT_ID, message)


    @classmethod
    def writeJSON(cls, result):

        filePath = "./data/notionDatabaseHolder.json"
        if NotionProterties.PRICE in result.keys():
            filePath = "./data/notionDatabaseBillHolder.json"

        with open(filePath, 'w', encoding='utf8') as fileData:
            json.dump(result, fileData, indent=4, ensure_ascii=False)


    @classmethod
    def fixFullText(cls, text, language='es'):

        if text != '':
            text = CheckGrammar.cleanStartAndEnd(text)
            if language == 'es':
                text = CheckGrammar.checkGrammar(text, language)
                text = CheckGrammar.checkPuntuaction(text)
                text = CheckGrammar.checkGrammar(text, language)
            elif language == 'en':
                text = CheckGrammar.checkGrammar(text, language)

        # to remove ending point
        return text[:-1]


    @classmethod
    def checkDestinationFolderExist(cls, path):

        try:
            print(path)
            subPath = os.path.dirname(path)
            if not os.path.exists(subPath):
                cls.checkDestinationFolderExist(subPath)
            if not os.path.exists(path):
                os.mkdir(path)
        except RuntimeError as error:
            cls.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def getDictData(cls, message, keysToCheck):

        dictResult = {}
        message = message.lower()

        for key in keysToCheck:
            startIndex = message.find(key.lower())

            endIndex = startIndex + len(key)
            startIndexNextProperty = -1

            nearestIndex = float('inf')
            for nextkey in keysToCheck:
                index = message[:].find(nextkey.lower())
                if key != nextkey and endIndex < index < nearestIndex:
                    startIndexNextProperty = index
                    nearestIndex = index

            value = message[endIndex:startIndexNextProperty]
            if startIndexNextProperty == -1:
                value = message[endIndex:]

            finalValue = CheckGrammar.cleanStartAndEnd(value).capitalize()
            dictResult.update({key: finalValue})

        return dictResult
