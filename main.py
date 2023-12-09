'''Main management class'''
import subprocess
import speech_recognition


from utils import Utils
from telegramBot import TelegramBot
from definitions import Obsidian, NotionIDs
from notionAPI import NotionApi
from todoistAPI import TodoistApi
from obsidianAPI import ObsidianApi
from definitions import Help

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


@TelegramBot.instance.message_handler(commands=['guia'])
def commandHelp(messageObject):
    '''Send help and info about the commands and his format'''
    Utils.sendMessage(Help.MESSAGE)

# @TelegramBot.instance.message_handler(commands=['gastos'])
# def commandExpense(messageObject):
#     '''Entry for page "Gastos"'''
#     Utils.sendMessage("GASTOS: -- ['cantidad' Titulo 'precio']")
#     NotionApi.createPage(NotionIDs.GASTOS, messageObject.text)


# @TelegramBot.instance.message_handler(commands=['diario'])
# def commandDiario(messageObject):
#     '''Entry for page "Diario"'''
#     Utils.sendMessage("DIARIO: -- [Titulo, Texto]")
#     NotionApi.createPage(NotionIDs.DIARIO, messageObject.text)


# @TelegramBot.instance.message_handler(commands=['multimedia'])
# def commandMedia(messageObject):
#     '''Entry for page "Multimedia"'''
#     Utils.sendMessage("MEDIA: -- [Titulo, Texto, Autor, Nota, Categoria]")
#     NotionApi.createPage(NotionIDs.MEDIA, messageObject.text)


# @TelegramBot.instance.message_handler(commands=['tarea'])
# def commandNewTask(messageObject):
#     '''Add a new task to Todoist'''
#     Utils.sendMessage("TAREAS: -- [Texto, Fecha, Proyecto, Repetir]")
#     TodoistApi.manageTodoistTask(messageObject.text)


@TelegramBot.instance.message_handler(commands=['nota'])
def commandNoteObsidian(messageObject):
    '''Create a new note in Obsidian'''
    Utils.sendMessage("REFERENCIAS: -- [retrieve tags from Obsidian]")
    ObsidianApi.initVault()
    ObsidianApi.createNote(messageObject)


@TelegramBot.instance.message_handler(commands=['update'])
def commandUpdate(messageObject):
    '''Update the API on the Raspberry'''
    print(f'Update')


# Handler messages
@TelegramBot.instance.message_handler(content_types=['text'])
def message_handler(messageObject):

    if messageObject.text[0] == "/":
        TelegramBot.lastCommand = messageObject.text
        return
    
    if TelegramBot.lastCommand == "/gastos":
        NotionApi.createPage(NotionIDs.GASTOS, messageObject.text)
        
    elif TelegramBot.lastCommand == "/diario":
        NotionApi.createPage(NotionIDs.DIARIO, messageObject.text)
        
    elif TelegramBot.lastCommand == "/media":
        NotionApi.createPage(NotionIDs.MEDIA, messageObject.text)
        
    elif TelegramBot.lastCommand == "/tarea":
        TodoistApi.manageTodoistTask(messageObject.text)


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
