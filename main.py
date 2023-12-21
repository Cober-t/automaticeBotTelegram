'''Main management class'''
import subprocess
import speech_recognition
import os

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils import Utils
from telegramBot import TelegramBot
from definitions import Obsidian, Todoist, DATAHOLDER, Help, COMMANDS

from notionAPI import NotionApi
from todoistAPI import TodoistApi
from obsidianAPI import ObsidianApi

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


@TelegramBot.instance.callback_query_handler(func=lambda call: True)
def menssageConstructor(call):

    TelegramBot.entryData = call.data

    if call.data == "Update":

        key = TelegramBot.lastCommand
        dictData = DATAHOLDER[key]

        # Notion pages
        if key in (COMMANDS.DIARIO, COMMANDS.GASTOS, COMMANDS.MEDIA):
            NotionApi.createPage(COMMANDS.NOTION_ID_DICT[key], dictData)
        
        # Todoist task
        elif key == COMMANDS.TAREA:

            # Handle links for title and description
            links = Utils.extractLinksFroMessage(dictData[Todoist.TITLE])
            if dictData[Todoist.DESCRIPTION] is not None:
                links.update(Utils.extractLinksFroMessage(dictData[Todoist.DESCRIPTION]))
                dictData[Todoist.DESCRIPTION] = dictData[Todoist.DESCRIPTION].text

            dictData[Todoist.TITLE] = dictData[Todoist.TITLE].text
            TodoistApi.manageTodoistTask(dictData, links)

        # Obsidian note
        elif key == COMMANDS.NOTA:

            ObsidianApi.initVault()
            ObsidianApi.createNote(dictData)
        

###################################
#||||||| HANDLER COMMANDS ||||||||#
###################################
@TelegramBot.instance.message_handler(commands=['diario', 'gastos', 'media', 'tarea', 'nota'])
def commandDiary(messageObject):    

    TelegramBot.lastCommand = messageObject.text

    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    for key in DATAHOLDER[TelegramBot.lastCommand]:
        DATAHOLDER[TelegramBot.lastCommand][key] = None
        markup.add(InlineKeyboardButton(key, callback_data=key))
    markup.add(InlineKeyboardButton("Crear Entrada", callback_data="Update"))

    TelegramBot.instance.send_message(messageObject.chat.id, "Rellena estos campos para crear la entrada", reply_markup=markup)


@TelegramBot.instance.message_handler(commands=['guia'])
def commandHelp(messageObject):
    '''Send help and info about the commands and his format'''
    Utils.sendMessage(Help.MESSAGE)


def getFolderStructure(path, ignoreFolders=None):

    if os.path.isfile(path):
        return ''

    subFolders = {}
    root = os.path.normpath(path).split("/")[-1]

    for folder in os.listdir(path):

        if ignoreFolders is not None and folder in ignoreFolders:
            continue

        subFoldersPath = os.path.join(path, folder)
        subFolders.update(getFolderStructure(subFoldersPath, ignoreFolders))

    dictFolder = { root: subFolders}

    return dictFolder


def formatMessage(folderStructure, ignoreFolders=None):

    root = list(folderStructure.keys())[0]
    message = formatMessageFolderStructure(root, folderStructure[root], ignoreFolders)
    return "~" + message[3:]


def formatMessageFolderStructure(folder, content, ignoreFolder, spaces=''):

    if ignoreFolder is not None and folder in ignoreFolder:
        return ''

    message = spaces[:-4] + "|--" + folder + "\n"

    subFolders = list(content.keys())
    for name in subFolders:

        space = "    " if name == subFolders[-1] else "|   "
        message += formatMessageFolderStructure(name, content[name], ignoreFolder, spaces + space)

    return message


@TelegramBot.instance.message_handler(commands=['carpetas'])
def commandPrintFolder(messageObject):
    '''Send help and info about the commands and his format'''
    folderStructure = getFolderStructure(Obsidian.VAULT_DIRECTORY, Obsidian.IGNORE_FOLDERS)
    Utils.sendMessage(formatMessage(folderStructure))


@TelegramBot.instance.message_handler(commands=['etiquetas'])
def commandPrintTags(messageObject):
    '''Send help and info about the commands and his format'''
    message = ''
    for tag in ObsidianApi.retrieveAllTags():
        message += tag + "\t"
    Utils.sendMessage(message[:-1])


@TelegramBot.instance.message_handler(commands=['update'])
def commandUpdate(messageObject):
    '''Update the API on the Raspberry'''
    import subprocess

    Utils.sendMessage(f"[INFO: Actualizando repositorio...]]")
    
    with subprocess.Popen(["python /home/pi/shared/Otros/updateRepository.py"], shell=True) as process:
        out, err = process.communicate()
        if out:
            Utils.sendMessage(out)
        if err:
            Utils.sendMessage(err)

    Utils.sendMessage(f"[INFO: Reiniciando server...]]")


@TelegramBot.instance.message_handler(commands=['boot'])
def commandBoot(messageObject):
    '''Update the API on the Raspberry'''
    import subprocess

    Utils.sendMessage(f"[INFO: Encendiendo ordenador...]]")
    
    with subprocess.Popen(["python /home/pi/shared/Otros/remoteBoot.py"], shell=True) as process:
        out, err = process.communicate()
        if out:
            Utils.sendMessage(out)
        if err:
            Utils.sendMessage(err)



###################################
#|||||||| HANDLER MESSAGES |||||||#
###################################
@TelegramBot.instance.message_handler(content_types=['text'])
def message_handler(messageObject):

    page = TelegramBot.lastCommand
    entry = TelegramBot.entryData
    
    if page in COMMANDS.KEYS:
        DATAHOLDER[page][entry] = messageObject.text

        if page == COMMANDS.TAREA and (entry == Todoist.TITLE or entry == Todoist.DESCRIPTION):
            DATAHOLDER[page][entry] = messageObject

        if page == COMMANDS.NOTA and entry == Obsidian.TEXT:
            DATAHOLDER[page][entry] = messageObject


###################################
#||||||| HANDLER RESOURCES |||||||#
###################################
def saveResourceInObsidian(filePath, name, downloadedFile):

    page = TelegramBot.lastCommand
    entry = TelegramBot.entryData

    if page == COMMANDS.NOTA and entry == Obsidian.RESOURCES:
        
        if DATAHOLDER[page][entry] is None:
            DATAHOLDER[page][entry] = [name]
        else:
            DATAHOLDER[page][entry].append(name)

        with open(filePath, 'wb') as document:
            document.write(downloadedFile)


@TelegramBot.instance.message_handler(content_types=['video'])
def message_handler(messageObject):

    try:
        downloadedFile, fileName = Utils.getFile(messageObject.video)
        if messageObject.caption:
            name = messageObject.caption + '.' + fileName.split('.')[-1]
        else:
            name = fileName
        
        filePath = Obsidian.VAULT_DIRECTORY + "/Resources/Videos/" + name
        saveResourceInObsidian(filePath, name, downloadedFile)

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

        filePath = Obsidian.VAULT_DIRECTORY + "/Resources/Documents/" + name

        saveResourceInObsidian(filePath, name, downloadedFile)

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

        filePath = Obsidian.VAULT_DIRECTORY + "/Resources/Images/" + name

        saveResourceInObsidian(filePath, name, downloadedFile)

    except TypeError as error:
        Utils.sendMessage(f"[ERROR : {error}]")


@TelegramBot.instance.message_handler(content_types=['voice'])
def voice_handler(messageObject):
    fileId = messageObject.voice.file_id
    fileData = TelegramBot.instance.get_file(fileId)

    downloadFile = TelegramBot.instance.download_file(fileData.file_path)

    sourceFile = os.path.abspath("media/audio.ogg")
    outputFile = os.path.abspath("media/audio.wav")

    with open(sourceFile, 'wb') as file:
        file.write(downloadFile)

    subprocess.run(['ffmpeg', '-i', sourceFile, outputFile, '-y'])
    fileData = speech_recognition.AudioFile(outputFile)
    with fileData as source:
        try:
            recognizer = speech_recognition.Recognizer()
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='es_ES')
            text = Utils.fixFullText(text)
            Utils.sendMessage(text)

        except TypeError as error:
            Utils.sendMessage(f"[ERORR : {error}]")


TelegramBot.inifinityPolling()
