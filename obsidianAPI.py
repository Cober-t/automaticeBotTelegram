import os
import re

from telebot.types import MessageEntity
from mdutils import MdUtils
from checkGrammarText import CheckGrammar
from datetime import date

# https://github.com/didix21/mdutils
from utils import Utils

# https://github.com/mfarragher/obsidiantools
from definitions import Obsidian
import obsidiantools.api as obsAPI


class ObsidianApi:

    vault = None

    @classmethod
    def initVault(cls):
        ObsidianApi.vault = obsAPI.Vault(Obsidian.VAULT_DIRECTORY).connect().gather()
        return ObsidianApi.vault


    @classmethod
    def getVault(cls):
        if not ObsidianApi.vault:
            Utils.sendMessage("[INFO: Building Obsidian vault...]")
            ObsidianApi.initVault()
        return ObsidianApi.vault


    @classmethod
    def createNote(cls, messageObject):

        folder, title, text, tags, links = ObsidianApi.extractDataFromMessage(messageObject)
        
        folderPath = os.path.normpath(Obsidian.VAULT_DIRECTORY + f"\\{folder}")
        Utils.checkDestinationFolderExist(folderPath)
        filePath = os.path.normpath(folderPath + f'\\{title}.md')

        try:
            newFile = MarkDownFileUtils(filePath)
            newFile.createNote(text, tags, links)
        except RuntimeError as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def extractDataFromMessage(cls, messageObject):

        links = {}
        if messageObject.entities:
            entities = MessageEntity.to_list_of_dicts(messageObject.entities)

        for entity in entities:
            startIndex = entity["offset"]
            endIndex = startIndex + entity["length"]
            hiperlink = text[startIndex: endIndex]
            link = entity["url"]
            links.update({hiperlink: link})
        
        text = CheckGrammar.cleanStartAndEnd(messageObject.text)
        obsidianDict = Utils.getDictData(messageObject.text, Obsidian.KEYS)

        for key in Obsidian.KEYS:
            try:
                value = obsidianDict[key]
                if value is None:
                    Utils.sendMessage(f"[ERROR: {key} value is empty]")
            except IndexError as error:
                Utils.sendMessage(f"[ERROR: incorrect value for {key}: ({error})]")    
        
        return  obsidianDict[Obsidian.FOLDER],\
                obsidianDict[Obsidian.TITLE],\
                obsidianDict[Obsidian.TEXT],\
                obsidianDict[Obsidian.TAGS].split(),\
                links
      

    @classmethod
    def retrieveTags(cls, note):
        return ObsidianApi.getVault().get_tags(note)
    

    @classmethod
    def retrieveAllTags(cls):
        tagsInFileNames = ObsidianApi.getVault().tags_index

        result = []
        for fileName in tagsInFileNames:
            for tag in tagsInFileNames[fileName]:
                if tag not in result:
                    result.append(tag)
    
        return sorted(result)


class MarkDownFileUtils:
    '''Utils for manage files from Obsidian'''

    mdFile = None
    todayDate = None
    allTags = []
    references = []

    @classmethod
    def __init__(cls, path):
        
        MarkDownFileUtils.mdFile = MdUtils(file_name=path)
        MarkDownFileUtils.todayDate = str(date.today())


    @classmethod
    def createNote(cls, text, tags, links):

        MarkDownFileUtils.writeText(text, tags, links)
        try:
            MarkDownFileUtils.mdFile.create_md_file()
        except RuntimeError as error:
            Utils.sendMessage(f"[ERROR: create new fileNote error {error}")


    @classmethod
    def writeText(cls, text, tags, links):

        headerLevel = 1
        newFile = MarkDownFileUtils.mdFile
        noteTags = ObsidianApi.vault.tags_index
        
        if newFile is None:
            return

        for nameFile in noteTags:
            # Format text word with a link to the note
            if nameFile in text:
                re.sub(nameFile, f"[[{nameFile}]]", text)
                MarkDownFileUtils.references.append(f'[[{nameFile}]]')

        sorted(MarkDownFileUtils.references)
        
        try:
            newFile.new_header(level=headerLevel, title='Fecha:', style='setext')
            newFile.new_line(MarkDownFileUtils.todayDate)
            newFile.new_line()

            if tags:
                newFile.new_header(level=headerLevel, title=f'Etiquetas:', style='setext')
                for tag in tags:
                    newFile.write(f'#{tag.lower()} ')
                newFile.new_line()

            newFile.new_header(level=headerLevel, title=f'Texto:', style='setext')
            newFile.write(text=text + '\n')
            newFile.new_line()
            
            if MarkDownFileUtils.references:
                newFile.new_header(level=headerLevel, title=f'Referencias:', style='setext')
                references = MarkDownFileUtils.references
                for i in range (0, len(references) - 1):
                    newFile.write(text=f"{references[i]}, ")
                
                newFile.write(text=MarkDownFileUtils.references[-1])
                newFile.new_line()

            if links:
                newFile.new_header(level=headerLevel, title=f'Enlaces:', style='setext')
                for text in list(links.keys()):
                    url = links[text]
                    newFile.new_line(newFile.new_inline_link(link=url, text=text.capitalize()))

            
        except RuntimeError:
            Utils.sendMessage("[ERROR: bad formating text]")
