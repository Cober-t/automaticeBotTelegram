'''Telegram API main message manager'''

from utils import Utils

from checkGrammarText import CheckGrammar
from notionAPI import NotionApi
from todoistAPI import TodoistApi
from obsidianAPI import ObsidianApi
from definitions import Help, NotionPages, Obsidian


class TelegramManager:

    @classmethod
    def manageMessage(cls, text):

        text = CheckGrammar.cleanStartAndEnd(text)

        choosenKey = None
        for key in Help.ALL_KEYS:
            textHolder = text.lower()

            if textHolder.find(key.lower()) == 0:
                choosenKey = key
                break

        if not choosenKey:
            return

        message = text[len(choosenKey):]

        if choosenKey in Help.GUIDE:
            Utils.sendMessage(Help.MESSAGE)

        elif key in NotionPages.KEYS:
            databaseID = NotionPages.KEYS[key]
            NotionApi.createPage(databaseID, key, message)

        elif key in ("Referencia", "Referencias"):
                
                obsidianDict = ObsidianApi.manageMessage(message)

                if obsidianDict:
                    path = obsidianDict[Obsidian.FOLDER]
                    title = obsidianDict[Obsidian.TITLE]
                    text = obsidianDict[Obsidian.TEXT]
                    tags = obsidianDict[Obsidian.TAGS].split()

                    ObsidianApi.createNote(path, title, text, tags)
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
