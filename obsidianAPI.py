import os
import re

from mdutils import MdUtils
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
    def createNote(cls, folder, title, text, tags=None, links=None):
        
        folderPath = os.path.normpath(Obsidian.VAULT_DIRECTORY + f"\\{folder}")

        Utils.checkDestinationFolderExist(folderPath)

        filePath = os.path.normpath(folderPath + f'\\{title}.md')

        try:
            newFile = MarkDownFileUtils(filePath)
            newFile.createNote(text, tags, links)
        except RuntimeError as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def manageMessage(cls, message):
        
        return Utils.getDictData(message, Obsidian.KEYS) if message else None
      

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

        text = MarkDownFileUtils.formatText(text, tags)

        MarkDownFileUtils.writeText(text, tags, links)
        try:
            MarkDownFileUtils.mdFile.create_md_file()
        except RuntimeError as error:
            Utils.sendMessage(f"[ERROR: create new fileNote error {error}")


    @classmethod
    def formatText(cls, text, tags):
        newFile = MarkDownFileUtils.mdFile
        if newFile is None:
            return

        noteTags = ObsidianApi.vault.tags_index

        for nameFile in noteTags:

            # Format text word with a link to the note
            if nameFile in text:
                re.sub(nameFile, f"[[{nameFile}]]", text)
                MarkDownFileUtils.references.append(f'[[{nameFile}]]')

        sorted(MarkDownFileUtils.references)

        return text

    @classmethod
    def writeText(cls, text, tags, links):

        headerLevel = 1
        newFile = MarkDownFileUtils.mdFile
        
        if newFile is None:
            return
        
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
