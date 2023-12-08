'''Telegram API main message manager'''

from utils import Utils

from telebot.types import MessageEntity
from checkGrammarText import CheckGrammar
from notionAPI import NotionApi
from todoistAPI import TodoistApi
from obsidianAPI import ObsidianApi
from definitions import Help, NotionPages, Obsidian


class TelegramManager:

    @classmethod
    def manageMessage(cls, messageObject):

        links = {}
        text = messageObject.text

        if messageObject.entities:
            entities = MessageEntity.to_list_of_dicts(messageObject.entities)

            for entity in entities:
                startIndex = entity["offset"]
                endIndex = startIndex + entity["length"]
                hiperlink = text[startIndex: endIndex]
                link = entity["url"]
                links.update({hiperlink: link})

        text = CheckGrammar.cleanStartAndEnd(messageObject.text)

        choosenKey = None
        for key in Help.ALL_KEYS:
            textHolder = text

            if textHolder.lower().find(key.lower()) == 0:
                choosenKey = key
                break

        if not choosenKey:
            return

        message = text[len(choosenKey):]

        if choosenKey in Help.GUIDE:
            Utils.sendMessage(Help.MESSAGE)

        elif choosenKey in NotionPages.KEYS:
            databaseID = NotionPages.KEYS[key]

            if message != '':
                NotionApi.createPage(databaseID, key, message)
            else:
                Utils.sendMessage(f"[Error: not message]")

        elif choosenKey in ("Notas, Nota"):
            
            ObsidianApi.initVault()
            obsidianDict = ObsidianApi.manageMessage(message)

            if obsidianDict:

                try:
                    folder = obsidianDict[Obsidian.FOLDER]
                    title = obsidianDict[Obsidian.TITLE]
                    text = obsidianDict[Obsidian.TEXT]
                    tags = obsidianDict[Obsidian.TAGS].split()

                except IndexError as error:
                    Utils.sendMessage(f"[ERROR: incorrect key value ({error})]")

                if folder is None:
                    Utils.sendMessage(f"[ERROR: folder value is empty]")
                    return

                if text is None:
                    Utils.sendMessage(f"[ERROR: text field is empty]")
                    return 
                
                ObsidianApi.createNote(folder, title, text, tags, links)
            else:
                Utils.sendMessage(f"[ERROR: Message does not exist]")

        elif key in ("Tarea", "Tareas"):
                TodoistApi.manageTodoistTask(message)
                # ...
                # Twitter API
                # Instagram API
                # Tik tok API
                # Bullet journal
                # Some estadistics
                # ...
        else:
            Utils.sendMessage(f"[ERROR: Key {key} invalid]")
