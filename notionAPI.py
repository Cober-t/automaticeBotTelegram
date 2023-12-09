'''Main Notion Class'''
import re
import json
from notion_database.page import Page
from notion_database.search import Search
from notion_database.database import Database
from notion_database.properties import Properties

from utils import Utils
from checkGrammarText import CheckGrammar
from definitions import NotionIDs, NotionJsonHolder, NotionProperties


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
    def createPage(cls, ID, message):

        message = message.lower()
        fileData = Utils.getDictData(message, NotionProperties.PROPERTIES)

        if ID is NotionIDs.GASTOS:

            message = CheckGrammar.cleanStartAndEnd(message).split(' ')

            fileData[NotionProperties.AMOUNT]= message[0]
            fileData[NotionProperties.TITLE] = message[1]
            fileData[NotionProperties.PRICE] = message[2]

            properties = NotionApi.createProperties(fileData)
            NotionUtils.createPage(ID, properties)
            return

        for propertyName in NotionProperties.PROPERTIES:

            if fileData[propertyName] is None or propertyName not in NotionUtils.getPropertyNames(ID):
                continue

            # Multiple options
            if NotionProperties.TAGS[0] in fileData and propertyName == fileData[NotionProperties.TAGS]:
                tagsList = [tag for tag in NotionUtils.getTagValues(ID) if tag.lower() in fileData[propertyName]]
                fileData[propertyName] = tagsList

            # Only one option
            if NotionProperties.CATEGORY[0] in fileData in propertyName == fileData[NotionProperties.CATEGORY]:
                tag = NotionUtils.getTagValues(ID)
                fileData[propertyName] = tag in fileData[propertyName]

        properties = NotionApi.createProperties(fileData)
        NotionUtils.createPage(ID, properties)


    @classmethod
    def createProperties(cls, fileData):

        newProperty = NotionProperty()
        
        title = Utils.fixFullText(fileData[NotionProperties.TITLE])
        newProperty.setTitle(title)
    
        if fileData[NotionProperties.TEXT] is not None:
            text = Utils.fixFullText(fileData[NotionProperties.TEXT])
            newProperty.setText(text)
    
        if fileData[NotionProperties.CATEGORY] is not None:
            newProperty.setSelect(fileData[NotionProperties.CATEGORY])
        
        if fileData[NotionProperties.TAGS] is not None:
            newProperty.setMultiSelect(fileData[NotionProperties.CATEGORY])
        
        if fileData[NotionProperties.AUTHOR] is not None:
            newProperty.setText(fileData[NotionProperties.AUTHOR])

        if fileData[NotionProperties.AMOUNT] is not None:
            newProperty.setNumber(NotionProperties.AMOUNT, int(fileData[NotionProperties.AMOUNT]))
        
        if fileData[NotionProperties.PRICE] is not None:
            price = fileData[NotionProperties.PRICE].replace(',', '.')
            newProperty.setNumber(NotionProperties.PRICE, float(price))

        if fileData[NotionProperties.RATING] is not None:
            rating = fileData[NotionProperties.RATING].replace(',', '.')
            newProperty.setNumber(NotionProperties.RATING, float(rating))

        return newProperty.property


    # @classmethod
    # def queueNotionTaskManager(cls):

    #     projects = cls.getPagesDatabase(NotionIDs.TASK_LIST)

    #     # Check all projects
    #     for projectName in projects: # pylint: disable=C0206
    #         projectTasks = projects[projectName]

    #         if 'Done' in projectTasks[0] and not projectTasks[0]['Done']:

    #             url = projectTasks[0]['URL']
    #             taskTitle = projectTasks[0]['Titulo']
    #             periodicity = projectTasks[0]['Periodicidad']

    #             projectID = TodoistApi.getProjectID(projectName)

    #             todoistTasksNow = ''
    #             todoistTasks = TodoistApi.getProjectTasks(projectID)
    #             while todoistTasks != todoistTasksNow:
    #                 todoistTasksNow = todoistTasks
    #                 todoistTasks = TodoistApi.getProjectTasks(projectID)

    #             # Check all tasks in the notion project
    #             for task in todoistTasks:
    #                 if taskTitle in task.content:
    #                     return

    #             content = taskTitle
    #             if url is not None:
    #                 content = f"[{taskTitle}]({url})"
    #             TodoistApi.addTask(name=content, projectID=projectID, repeat=periodicity)

    #             propertyUpdated = NotionProperty()
    #             propertyUpdated.setCheckbox(True)

    #             NotionUtils.retrieveDatabase(NotionIDs.TASK_LIST)
    #             NotionUtils.updateDatabase(NotionIDs.TASK_LIST, taskTitle, propertyUpdated)


    # @classmethod
    # def getPagesDatabase(cls, databaseID):

    #     pages = {}
    #     pagesRetrieved = NotionUtils.findPage(databaseID, 100)

    #     if not pagesRetrieved:
    #         return None

    #     for page in pagesRetrieved:
    #         newPage = {'ID': {page['id']}}
    #         properties = page['properties']
    #         proyect = page['properties'][Todoist.PROJECT]['select']
    #         proyectName = proyect['name']

    #         if proyect is None:
    #             continue

    #         if proyectName not in pages.keys():
    #             pages.update({proyectName: []})

    #         for propertyName in properties:

    #             pageType = pageProp['type']
    #             pageProp = properties[propertyName]

    #             if pageType == 'date' and pageProp['date'] is not None:
    #                 newPage.update({propertyName: pageProp['date']['start']})

    #             elif pageType == 'rich_text' and pageProp['rich_text'] != []:
    #                 newPage.update({propertyName: pageProp['rich_text'][0]['text']['content']})

    #             elif pageType == 'title' and pageProp['title'] != []:
    #                 newPage.update({propertyName: pageProp['title'][0]['text']['content']})

    #             elif pageType == 'url':
    #                 newPage.update({propertyName: pageProp['url']})

    #             elif pageType == 'checkbox':
    #                 newPage.update({propertyName: pageProp['checkbox']})

    #         pages[proyectName].append(newPage)

    #     return pages


# queueNotionTaskManager()
