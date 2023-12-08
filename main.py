'''Main management class'''
import subprocess
import speech_recognition

from utils import Utils
from telegramBot import TelegramBot
from telegramAPI import TelegramManager
from definitions import Obsidian
from notionAPI import NotionApi


# # Check daily tasks
# dtToday = datetime.today()
# dtTomorrow = dtToday.replace(day=dtToday.day+1, hour=7, minute=0, second=0, microsecond=0)
# deltaT = dtTomorrow - dtToday

# secs=deltaT.seconds+1

# def checkDailyTasks():
#     NotionApi.queueNotionTaskManager()

# timer = Timer(secs, checkDailyTasks)
# timer.start()


TelegramBot.initBot()

# Handler messages
@TelegramBot.instance.message_handler(content_types=['video'])
def message_handler(messageObject):

    try:
        downloadedFile, fileName = Utils.getFile(messageObject.video)
        if messageObject.caption:
            name = messageObject.caption + '.' + fileName.split('.')[-1]
        else:
            name = fileName
        
        filePath = Obsidian.VAULT_DIRECTORY + "/Resources/" + name

        with open(filePath, 'wb') as document:
            document.write(downloadedFile)
    except TypeError as error:
        Utils.sendMessage(f"[ERROR : {error}]")


@TelegramBot.instance.message_handler(content_types=['document'])
def message_handler(messageObject):

    try:
        downloadedFile, fileName = Utils.getFile(messageObject.document)
        if messageObject.caption:
            name = messageObject.caption + '.' + fileName.split('.')[-1]
        else:
            name = messageObject.document.file_name

        filePath = Obsidian.VAULT_DIRECTORY + "/Resources/" + name

        with open(filePath, 'wb') as document:
            document.write(downloadedFile)

    except TypeError as error:
        Utils.sendMessage(f"[ERROR : {error}]")


@TelegramBot.instance.message_handler(content_types=['photo'])
def message_handler(messageObject):

    try:
        downloadedFile, fileName = Utils.getFile(messageObject.photo[-1])
        if messageObject.caption:
            name = messageObject.caption + '.' + fileName.split('.')[-1]
        else:
            name = fileName

        filePath = Obsidian.VAULT_DIRECTORY + "/Resources/" + name

        with open(filePath, 'wb') as photoFile:
            photoFile.write(downloadedFile)

    except TypeError as error:
        Utils.sendMessage(f"[ERROR : {error}]")


@TelegramBot.instance.message_handler(content_types=['text'])
def message_handler(messageObject):

    try:
        TelegramManager.manageMessage(messageObject)
    except TypeError as error:
        Utils.sendMessage(f"[ERROR : {error}]")


# @TelegramBot.instance.message_handler(content_types=['voice'])
# def voice_handler(message):
#    fileId = message.voice.file_id
#    fileData = TelegramBot.instance.get_file(fileId)

#    downloadFile = TelegramBot.instance.download_file(fileData.file_path)

#    with open('./media/audio.ogg', 'wb') as file:
#        file.write(downloadFile)

#    subprocess.run(['ffmpeg', '-i', './media/audio.ogg', './media/audio.wav', '-y'])
#    fileData = speech_recognition.AudioFile('./media/audio.wav')


#    try:
#        recognizer = speech_recognition.Recognizer()
#        audio = recognizer.record(fileData)
#        text = recognizer.recognize_google(audio, language='es_ES')
#        TelegramManager.manageMessage(text)

#    except TypeError as error:
#        Utils.sendMessage(f"[ERORR : {error}]")


TelegramBot.inifinityPolling()
