import os

# https://github.com/didix21/mdutils
from mdutils import MdUtils

from datetime import date

from utils import Utils

# https://github.com/mfarragher/obsidiantools
from definitions import Obsidian
import obsidiantools.api as obsAPI

# TODO:
# Crear notas en el path indicado, si no existe el path crearlo
# Crear la nota añadiendo información en los campos 'Data', 'Tags', 'Summary' y 'References'

# Para 'References' devolver listado de otras notas con mayor coincidencia de etiquetas

# Crear índice de etiquetas
# Si se recive una etiqueta que no está en el índice añadir a este

class ObsidianApi:

    vault = None

    @classmethod
    def initVault(cls):
        ObsidianApi.vault = obsAPI.Vault(Obsidian.VAULT_DIRECTORY).connect().gather()
        return ObsidianApi.vault


    @classmethod
    def getVault(cls):
        if not ObsidianApi.vault:
            print("[INFO: Building Obsidian vault...]")
            # Utils.sendMessage("[INFO: Building Obsidian vault...]")
            cls.initVault()
        return ObsidianApi.vault


    @classmethod
    def createNote(cls, folder, title, text, tags=None):

        today = date.today()
        fullPath = os.path.normpath(Obsidian.VAULT_DIRECTORY + folder)
        Utils.checkDestinationFolderExist(fullPath)
        filePath = os.path.normpath(fullPath + '\\ejemplooooo.md')
        # fileName = os.path.basename(fullPath) + f'{title}.md'


        try:
            with open(filePath, 'w', encoding='utf8') as f:
                f.write(cls.getVault().get_source_text("template"))
        except RuntimeError as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def manageMessage(cls, message):
        
        return Utils.getDictData(message, Obsidian.KEYS) if message else None
      
    @classmethod
    def retrieveTags(cls, note):
        return ObsidianApi.getVault().get_tags(note)


    # @classmethod
    # def retrieveHeaderConten():


print(ObsidianApi.retrieveTags("Ejemplo"))
