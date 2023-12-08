'''Main definitions'''

# TelegramBot
class Telegram:
    CHAT_ID = 5915979478
    BOT_TOKEN = "6239437612:AAEle5IFdMBBwzPudIVfRgkj_JKHh2bMxIY"


# METHEODATA
class MetheoData:
    LOCATION_POINT = {
        "lat":  40.3911717, 
        "long": -3.6951902, 
        "alt":  654.1
        }


# OBSIDIAN
class Obsidian:
    VAULT_DIRECTORY = "C:/Users/Jorge/Documents/ObsidianVault"  # \\Cober\coberstorage\ObsidianVault\
    NOTE_HOLDER = VAULT_DIRECTORY + "/test.md" # \\Cober\coberstorage\ObsidianVault\test.md
    NOTE_TEMPLATE = "##Date: {{date}}\n ##Tags: \n ##Summary: \n ##References:"
    FOLDER = 'Carpeta'
    TEXT = 'Texto'
    TITLE = 'Titulo'
    TAGS = 'Etiquetas'
    KEYS = [FOLDER, TEXT, TITLE, TAGS]


# TODOIST
class Todoist:
    DESCRIPTION = "Texto"
    PROJECT = "Proyecto"
    REPEAT = "Repetir"
    DATE = "Fecha"
    TOKEN = "f290c9540c7063f6378da720e097f79959afda2b"
    PROJECT_DEV = "2248977832"
    PROJECT_3D = "2249295933"
    PROJECT_ANATOMIA = "2210170147"
    PROJECT_VALOR = "2248974110"
    INBOX_ID = "2210170146"


class NotionIDs:
    PAGE_ID= "a6b2c97738a34e7ab49eb52ec61295bf"
    TOKEN  = "secret_xIG8raDuQGnWIOBeZcPDT1lxwPt11saBZ7nha3bsJcf"
    NOTAS  = "b34feafacc394e578c821821bf066587"
    DIARIO = "cf0b2cc9a4d247fcad28ec1fa3fb6b35"
    APUNTES= "36a02cde85fa4b99b50862f1173cd9a2"
    GASTOS = "e6ce65daad354873a1a9185c9392a7c4"
    MEDIA  = "6dcd686f2d174a8d9fbe31c2ad7b380f"
    TASK_LIST  = "116fab72255b40328062fb34bc01e12c"


class NotionProperties:
    TITLE = "Titulo"
    TEXT = "Texto"
    TAGS = "Etiquetas"
    AUTHOR = "Autor"
    PAGE = "Pagina"
    CATEGORY = "Categoria"
    AMOUNT = "Cantidad"
    PRICE = "Precio"
    PROPERTIES = [TITLE, TEXT, TAGS, AUTHOR, PAGE, CATEGORY]


class NotionPages:
    DIARIO = "Diario"
    APUNTES = "Apuntes"
    GASTOS = "Gastos"
    MEDIA = "Media"
    KEYS = {
        DIARIO: NotionIDs.DIARIO,
        APUNTES: NotionIDs.APUNTES,
        GASTOS: NotionIDs.GASTOS,
        MEDIA: NotionIDs.MEDIA
        }


class Help:

    GUIDE = ("Guía", "Guia")

    ALL_KEYS = ("Guía", "Guia", "Referencia", "Referencias", "Tarea", "Tareas", "Nota", "Notas",
                NotionPages.DIARIO, NotionPages.APUNTES, NotionPages.GASTOS, NotionPages.MEDIA)
    
    MESSAGE = "Formato de los comandos: \n\
    \t\tDIARIO: -- [Titulo, Texto]\n\n\
    \t\tAPUNTES: -- [Titulo, Texto, Autor, Pagina]\n\n\
    \t\tMEDIA: -- [Titulo, Texto, Autor, Nota, Categoria]\n\n\
    \t\tTAREAS: -- [Texto, Fecha, Proyecto, Repetir]\n\n\
    \t\tGASTOS: -- ['cantidad' Titulo 'precio']\n\n\
    \t\tNOTAS: -- [Carpeta, Titulo, Texto, Etiquetas]\n\n\
    \t\tREFERENCIAS: -- [retrieve tags from Obsidian]"


class JsonHolder:
    DEFAULT_JSON = {
        "Titulo": "None",
        "Texto": "None",
        "Etiquetas": [],
        "Autor": "None",
        "Nota": -1,
        "Pagina": -1,
        "Categoria": "None"
    }

    DEFAULT_JSON_BILL = {
        "Titulo": [],
        "Cantidad": [],
        "Precio": []
    }
