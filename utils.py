'''Main Utils class'''
import os
import json

from definitions import Telegram, NotionProperties
from checkGrammarText import CheckGrammar
from telegramBot import TelegramBot


class Utils:


    @classmethod
    def sendMessage(cls, message):

        TelegramBot.instance.send_message(Telegram.CHAT_ID, message)


    @classmethod
    def fixFullText(cls, text, language='es'):

        if text != '' and text is not None:
            text = CheckGrammar.cleanStartAndEnd(text)
            if language == 'es':
                text = CheckGrammar.checkGrammar(text, language)
                # text = CheckGrammar.checkPuntuaction(text)
                # text = CheckGrammar.checkGrammar(text, language)
            elif language == 'en':
                text = CheckGrammar.checkGrammar(text, language)

        return text


    @classmethod
    def checkDestinationFolderExist(cls, path):

        try:
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
        rawMessage = message
        message = message.lower()

        for key in keysToCheck:
            startIndex = message.find(key.lower())
            if startIndex == -1:
                dictResult.update({key: None})
                continue

            endIndex = startIndex + len(key)
            startIndexNextProperty = -1

            nearestIndex = float('inf')
            for nextkey in keysToCheck:
                index = message[:].find(nextkey.lower())
                if key != nextkey and endIndex < index < nearestIndex:
                    startIndexNextProperty = index
                    nearestIndex = index

            value = rawMessage[endIndex:startIndexNextProperty]
            if startIndexNextProperty == -1:
                value = rawMessage[endIndex:]

            finalValue = CheckGrammar.cleanStartAndEnd(value)
            finalValue = finalValue[0].capitalize() + finalValue[1:]
            dictResult.update({key: finalValue})

        return dictResult
    

    @classmethod
    def getFile(cls, fileObject):
        fileID = fileObject.file_id
        fileInfo = TelegramBot.instance.get_file(fileID)
        fileName = fileInfo.file_path.split('/')[-1]
        downloadedFile = TelegramBot.instance.download_file(fileInfo.file_path)

        return downloadedFile, fileName