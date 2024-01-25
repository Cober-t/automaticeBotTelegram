'''Main Notion Class'''
from notion_database.page import Page
from notion_database.search import Search
from notion_database.database import Database
from notion_database.properties import Properties

from utils import Utils
from checkGrammarText import CheckGrammar
from definitions import NotionIDs, NotionProperties


# FOR PAGES
# PROPERTY = Properties()
# PROPERTY.set_title("title", "title")
# FOR DATABASE
# PROPERTY = Properties()
# PROPERTY.set_title("title")

###################################
#||||||||| PROPERTY UTILS ||||||||#
###################################
class NotionProperty():

    def __init__(self):
        self.property = Properties()

    def setTitle(self, title):
        self.property.set_title(NotionProperties.TITLE, title)

    def setText(self, text):
        self.property.set_rich_text(NotionProperties.TEXT, text)
    
    def setAuthor(self, text):
        self.property.set_rich_text(NotionProperties.AUTHOR, text)

    def setSelect(self, selectOption):
        self.property.set_select(NotionProperties.CATEGORY, selectOption)

    def setMultiSelect(self, tags):
        self.property.set_multi_select(NotionProperties.TAGS, tags)

    def setNumber(self, key, number):
        self.property.set_number(key, number)
    
    def setCheckbox(self, checked):
        self.property.set_checkbox("checkbox", checked)


###################################
#||||||||||||| UTILS |||||||||||||#
###################################
class NotionUtils:
    S = Search(integrations_token=NotionIDs.TOKEN)
    P = Page(integrations_token=NotionIDs.TOKEN)
    D = Database(integrations_token=NotionIDs.TOKEN)


    @classmethod
    def getProperties(cls, ID):
        try:
            NotionUtils.D.retrieve_database(ID, get_properties=True)
            return NotionUtils.D.properties_list
        except (ValueError, TypeError) as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def getPropertyNames(cls, ID):
        return [properties["name"] for properties in cls.getProperties(ID)]


    @classmethod
    def getTagValues(cls, ID):
        values = []
        properties = cls.getProperties(ID)

        for propertyValue in properties:

            if propertyValue['name'] in (NotionProperties.TAGS, NotionProperties.CATEGORY):

                if "multi_select" in propertyValue.keys():
                    values = [option["name"] for option in propertyValue["multi_select"]["options"]]

                elif "select" in propertyValue.keys():
                    values = [option["name"] for option in propertyValue["select"]["options"]]

        return values


    @classmethod
    def createPage(cls, ID, properties):
        try:
            NotionUtils.P.create_page(database_id=ID, properties=properties)
        except (ValueError, TypeError) as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def retrieveDatabase(cls, ID, getProperties=True):
        try:
            NotionUtils.D.retrieve_database(database_id=ID, get_properties=getProperties)
        except (ValueError, TypeError) as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def findPage(cls, ID, pageSize):
        try:
            NotionUtils.D.find_all_page(database_id=ID, page_size=pageSize)
        except (ValueError, TypeError) as error:
            Utils.sendMessage(f"[ERROR: {error}]")

        if len(NotionUtils.D.result) > 0:
            return NotionUtils.D.result["result"]
        return None


    @classmethod
    def updateDatabase(cls, ID, title, newPropertiesToAdd):
        NotionUtils.D.update_database(database_id=ID, title=title, add_properties=newPropertiesToAdd)



###################################
#|||||||||||||| API ||||||||||||||#
###################################
class NotionApi:

    @classmethod
    def createPage(cls, ID, fileData):

        try:
            properties = NotionApi.createProperties(fileData)
            if properties:
                NotionUtils.createPage(ID, properties)
                Utils.sendMessage(f"[INFO: Entrada creada con exito!]")
            else:
                Utils.sendMessage(properties)
        except (RuntimeError, ValueError, IndexError) as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def createProperties(cls, fileData):

        newProperty = NotionProperty()
        
        for entryKey in fileData:
            value = fileData[entryKey]
            
            if entryKey is NotionProperties.TITLE:
                title = Utils.fixFullText(value)
                newProperty.setTitle(title)
                
            elif entryKey is NotionProperties.TEXT:
                text = Utils.fixFullText(value)
                newProperty.setText(text)

            elif entryKey is NotionProperties.TAGS:
                newProperty.setMultiSelect(value)

            elif entryKey is NotionProperties.CATEGORY:
                newProperty.setSelect(value)

            elif entryKey is NotionProperties.AUTHOR:
                newProperty.setAuthor(value)

            elif entryKey is NotionProperties.AMOUNT:
                if not value:
                    value = 1
                newProperty.setNumber(NotionProperties.AMOUNT, int(value))

            elif entryKey is NotionProperties.PRICE:
                if not value:
                    return "[ERROR: El campo de precio esta vacío o es invalido]"
                price = value.replace(',', '.')
                if price[0] != '+':
                    price = '-' + price
                newProperty.setNumber(NotionProperties.PRICE, float(price))

            elif entryKey is NotionProperties.RATING:
                rating = value.replace(',', '.')
                newProperty.setNumber(NotionProperties.RATING, float(rating))
            else:
                Utils.sendMessage(f"[ERROR: Invalid key data for {entryKey}]")

        return newProperty.property
