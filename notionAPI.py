'''Main Notion Class'''
import re
import json
from notion_database.page import Page
from notion_database.search import Search
from notion_database.database import Database
from notion_database.properties import Properties

from utils import Utils
from checkGrammarText import CheckGrammar
from todoistAPI import TodoistApi
from definitions import NotionIDs, NotionPages, NotionProterties, JsonHolder, Todoist


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
        self.property.set_title(NotionProterties.TITLE, title)

    def setText(self, text):
        self.property.set_rich_text(NotionProterties.TEXT, text)

    def setSelect(self, selectOption):
        self.property.set_select(NotionProterties.CATEGORY, selectOption)

    def setMultiSelect(self, tags):
        self.property.set_multi_select(NotionProterties.TAGS, tags)

    def setNumber(self, number):
        self.property.set_number(NotionProterties.PAGE, number)
    
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
    def getTagsPropertyValues(cls, ID):
        values = []
        properties = cls.getProperties(ID)

        for propertyValue in properties:

            if propertyValue['name'] in (NotionProterties.TAGS, NotionProterties.CATEGORY):

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
    def getNotionJSONHolder(cls):
        try:
            with open("./data/notionDatabaseHolder.json", 'r', encoding='utf8') as fileData:
                data = json.load(fileData)
                fileData.close()
                return data
        except RuntimeError as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def getNotionJSONBillHolder(cls):
        try:
            with open("./data/notionDatabaseBillHolder.json", 'r', encoding='utf8') as fileData:
                data = json.load(fileData)
                fileData.close()
                return data
        except RuntimeError as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def createPage(cls, ID, key, message):

        Utils.writeJSON(JsonHolder.DEFAULT_JSON)
        Utils.writeJSON(JsonHolder.DEFAULT_JSON_BILL)

        if NotionPages.GASTOS in key:

            fileData = cls.getNotionJSONBillHolder()
            fileData = cls.formatGastos(fileData, message)
            Utils.writeJSON(fileData)
            cls.createBillProperties(ID, fileData)

        else:
            fileData = cls.getNotionJSONHolder()
            message = message.lower()

            databasePropertyNames = NotionUtils.getPropertyNames(ID)
            databasePropertyNames.append("Titulo")

            propertiesToCheck = []
            for propertyName in databasePropertyNames:
                if propertyName in NotionProterties.PROPERTIES and propertyName.lower() in message:
                    propertiesToCheck.append(propertyName)
                elif propertyName != "Created time":
                    Utils.sendMessage(f"[ERROR: Your message does not have the database property {propertyName}]")

            for propertyName in propertiesToCheck:
                startIndex = message.find(propertyName.lower())

                endIndex = startIndex + len(propertyName)
                startIndexNextProperty = -1

                nearestIndex = 10000
                for nextProperty in propertiesToCheck:
                    index = message[:].find(nextProperty.lower())
                    if propertyName != nextProperty and endIndex < index < nearestIndex:
                        startIndexNextProperty = index
                        nearestIndex = index

                value = message[endIndex:startIndexNextProperty]
                if startIndexNextProperty == -1:
                    value = message[endIndex:]

                value = CheckGrammar.cleanStartAndEnd(value).capitalize()

            # dictData = Utils.getDictData(message, propertiesToCheck)

                if propertyName == NotionProterties.NOTE or propertyName == NotionProterties.PAGE:
                    value = int(re.search(r'\d+', value)[0])

                elif propertyName == NotionProterties.TAGS:
                    tagsTask = []
                    tags = NotionUtils.getTagsPropertyValues(ID)
                    for tag in tags:
                        if tag.lower() in value.lower():
                            tagsTask.append(tag)
                    value = tagsTask

                elif propertyName == NotionProterties.CATEGORY:
                    tags = NotionUtils.getTagsPropertyValues(ID)
                    for tag in tags:
                        if tag in value:
                            value = tag

                fileData[propertyName] = value

            Utils.writeJSON(fileData)
            properties = cls.createProperties(key, fileData)
            NotionUtils.createPage(ID, properties)


    @classmethod
    def createBillProperties(cls, databaseID, file):
        titles = file[NotionProterties.TITLE]
        amounts = file[NotionProterties.AMOUNT]
        prices = file[NotionProterties.PRICE]

        if len(titles) == len(amounts) == len(prices):
            i = 0
            numPagesToCreate = len(titles)
            while i < numPagesToCreate:
                properties = Properties()
                properties.set_title(NotionProterties.TITLE, titles[i])
                properties.set_number(NotionProterties.AMOUNT, int(amounts[i]))
                properties.set_number(NotionProterties.PRICE, float(prices[i]))
                NotionUtils.P.create_page(database_id=databaseID, properties=properties)
                i += 1
        else:
            Utils.sendMessage("Bad formated JSON")


    @classmethod
    def createProperties(cls, key, fileData):

        newProperty = NotionProperty()
        title = Utils.fixFullText(fileData[NotionProterties.TITLE])
        text = Utils.fixFullText(fileData[NotionProterties.TEXT])

        newProperty.setTitle(title)
        newProperty.setText(text)

        if key == "Apuntes":
            newProperty.setText(fileData[NotionProterties.AUTHOR].capitalize())
            newProperty.setNumber(fileData[NotionProterties.PAGE])
        elif key == "Media":
            newProperty.setText(fileData[NotionProterties.AUTHOR].capitalize())
            newProperty.setNumber(fileData[NotionProterties.NOTE])
            newProperty.setSelect(fileData[NotionProterties.CATEGORY])

        return newProperty


    @classmethod
    def formatGastos(cls, fileData, message):
        i = 0
        text = ''
        message = CheckGrammar.cleanStartAndEnd(message).split(' ')

        for element in message:

            if element.lower() not in ('euro', 'euros'):

                if i == 0:
                    i = 1
                    fileData[NotionProterties.AMOUNT].append(int(CheckGrammar.cleanStartAndEnd(element)))

                elif not re.search('[0-9]', element):
                    text += element + ' '

                else:
                    text = Utils.fixFullText(text)
                    text = CheckGrammar.cleanStartAndEnd(text).capitalize()
                    fileData[NotionProterties.TITLE].append(text)

                    if "'" in element:
                        element = float(element.replace("'", '.'))
                    elif "," in element:
                        element = float(element.replace(',', '.'))

                    fileData[NotionProterties.PRICE].append(element)

        return fileData


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


    @classmethod
    def getPagesDatabase(cls, databaseID):

        pages = {}
        pagesRetrieved = NotionUtils.findPage(databaseID, 100)

        if not pagesRetrieved:
            return None

        for page in pagesRetrieved:
            newPage = {'ID': {page['id']}}
            properties = page['properties']
            proyect = page['properties'][Todoist.PROJECT]['select']
            proyectName = proyect['name']

            if proyect is None:
                continue

            if proyectName not in pages.keys():
                pages.update({proyectName: []})

            for propertyName in properties:

                pageType = pageProp['type']
                pageProp = properties[propertyName]

                if pageType == 'date' and pageProp['date'] is not None:
                    newPage.update({propertyName: pageProp['date']['start']})

                elif pageType == 'rich_text' and pageProp['rich_text'] != []:
                    newPage.update({propertyName: pageProp['rich_text'][0]['text']['content']})

                elif pageType == 'title' and pageProp['title'] != []:
                    newPage.update({propertyName: pageProp['title'][0]['text']['content']})

                elif pageType == 'url':
                    newPage.update({propertyName: pageProp['url']})

                elif pageType == 'checkbox':
                    newPage.update({propertyName: pageProp['checkbox']})

            pages[proyectName].append(newPage)

        return pages


# queueNotionTaskManager()
