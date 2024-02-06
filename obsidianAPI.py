import os, re

from mdutils import MdUtils
from checkGrammarText import CheckGrammar

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
        return ObsidianApi.initVault()


    @classmethod
    def createNote(cls, fileData):

        try:
            title = CheckGrammar.cleanStartAndEnd(fileData[Obsidian.TITLE])
            text = CheckGrammar.cleanStartAndEnd(fileData[Obsidian.TEXT].text)
            Obsidian.LAST_NOTE = title
            
            links = Utils.extractLinksFroMessage(fileData[Obsidian.TEXT])
            resources = fileData[Obsidian.RESOURCES]
        except (IndexError, AttributeError) as error:
            Utils.sendMessage(f"[ERROR: some fields are empty]")
            return

        tags = []
        for tag in fileData[Obsidian.TAGS].split(','):
            tag = CheckGrammar.cleanStartAndEnd(tag).replace(' ', '_')
            if tag not in tags:
                tags.append(tag)

        folderPath = os.path.normpath(Obsidian.VAULT_DIRECTORY + f"/{fileData[Obsidian.FOLDER]}")
        Utils.checkDestinationFolderExist(folderPath)
        filePath = os.path.normpath(folderPath + f'/{title}.md')

        try:
            newFile = MarkDownFileUtils(filePath)
            newFile.createNote(title, text, tags, links, resources)
        except RuntimeError as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def retrieveNote(cls, noteName):
        return ObsidianApi.getVault().get_readable_text(noteName)
    

    @classmethod
    def retrieveLastNote(cls):
        if not Obsidian.LAST_NOTE:
            return
        return ObsidianApi.retrieveNote(Obsidian.LAST_NOTE)
    

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

        return sorted(list(set(result)))


class MarkDownFileUtils:
    '''Utils for manage files from Obsidian'''

    mdFile = None
    allTags = []
    references = []

    @classmethod
    def __init__(cls, path):
        
        print(path)
        MarkDownFileUtils.mdFile = MdUtils(file_name=path)


    @classmethod
    def createNote(cls, title, text, tags, links, resources):

        try:
            MarkDownFileUtils.writeText(title, text, tags, links, resources)
            MarkDownFileUtils.mdFile.create_md_file()
        except (RuntimeError, ValueError, IndexError, AttributeError) as error:
            Utils.sendMessage(f"[ERROR: create new fileNote error - {error}")


    @classmethod
    def writeText(cls, title, text, tags, links, resources):

        headerLevel = 2
        newFile = MarkDownFileUtils.mdFile
        noteTags = ObsidianApi.vault.tags_index
        
        if newFile is None:
            return

        for nameFile in noteTags:
            # Format text word with a link to the note
            if nameFile in text:
                fileReferenced = f"[[{nameFile}]]"
                re.sub(nameFile, fileReferenced, text)
                if fileReferenced not in MarkDownFileUtils.references:
                    MarkDownFileUtils.references.append(fileReferenced)

        sorted(MarkDownFileUtils.references)
        
        try:
            newFile.new_header(level=1, title=title, style='setext')
            newFile.new_header(level=headerLevel, title='Fecha:', style='setext')
            newFile.new_line(str(Utils.todayDate()))
            newFile.new_line()

            if tags:
                newFile.new_header(level=headerLevel, title=f'Etiquetas:', style='setext')
                for tag in tags:
                    newFile.write(f'#{tag.lower()} ')
                newFile.new_line()

            newFile.new_header(level=headerLevel, title=f'Texto:', style='setext')
            newFile.write(text=text + '\n')
            newFile.new_line()

            if resources:
                newFile.new_header(level=headerLevel, title=f'Recursos:', style='setext')
                for resource in resources:
                    newFile.write(text=f"![[{resource}]]" + '\n')
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

        except RuntimeError as error:
            Utils.sendMessage(f"[ERROR: bad formating text {error}]")
