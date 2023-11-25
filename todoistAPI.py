'''Main Todoist Class'''
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync

from definitions import Todoist
from checkGrammarText import CheckGrammar
from utils import Utils

# TODO:
# Que una tarea pueda recibir fecha y url

###################################
#|||||||||||| HELPER |||||||1|||||#
###################################
class TodoistHelper:

    notionTopQueueTask = None
    apiAsync = TodoistAPIAsync(Todoist.TOKEN)
    api = TodoistAPI(Todoist.TOKEN)

    @classmethod
    async def getProjectsAsync(cls):
        return TodoistHelper.apiAsync.get_projects()

    @classmethod
    def getProjects(cls):
        return TodoistHelper.api.get_projects()

    @classmethod
    async def getTasksAsync(cls):
        return TodoistHelper.apiAsync.get_tasks()

    @classmethod
    def getTasks(cls):
        return TodoistHelper.api.get_tasks()

    @classmethod
    def addTask(cls, name, projectID=Todoist.INBOX_ID, repeat=None, date=None, url=''):
        try:
            # dueDate = {
            #     "date": "2023-06-30",
            #     "timezone": None,
            #     "is_recurring": True,
            #     "string": "tomorrow at 10:00",
            # }
            TodoistHelper.api.add_task(content=name, project_id=projectID, due_string=repeat)
        except Exception as error:
            Utils.sendMessage(f"[ERROR: {error} - ProjectName: {name} - ProjectID: {projectID}]")


###################################
#|||||||||||||| API ||||||||||||||#
###################################
class TodoistApi:


    @classmethod
    async def getProjectsAsync(cls):
        try:
            return await TodoistHelper.getProjectsAsync()
        except Exception as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def getProjectsSync(cls):
        try:
            return TodoistHelper.getProjects()
        except Exception as error:
            Utils.sendMessage(f"[ERROR: {error}]")


    @classmethod
    def getProjectTasks(cls, projectID="2210170146"):
        return [task for task in TodoistHelper.getTasks() if task.project_id == projectID]


    @classmethod
    def getProjectNames(cls):
        return [project.name for project in TodoistHelper.getProjects()]


    @classmethod
    def getProjectID(cls, projectName):
        for project in TodoistHelper.getProjects():
            if projectName.lower() == project.name.lower():
                return project.id

        return None


    @classmethod
    def manageTodoistTask(cls, message):

        description = Todoist.DESCRIPTION
        project = Todoist.PROJECT
        inboxID = Todoist.INBOX_ID
        repeat = Todoist.REPEAT
        date = Todoist.DATE

        message = message.lower()
        taskInfo = {description: '', project: inboxID, repeat:None}
        propertiesToCheck = [description, project, repeat, date]

        for currentProperty in propertiesToCheck:

            if currentProperty.lower() in message:
                startIndex = message.find(currentProperty.lower())

                if startIndex == -1:
                    Utils.sendMessage(f"[INFO: Your message does not have the database property {property} on it]")
                    continue

                endIndexCurrentProperty = startIndex + len(currentProperty)
                startIndexNextProperty = -1

                for nextProperty in propertiesToCheck:

                    if nextProperty != currentProperty:
                        index = message.find(nextProperty.lower())
                        
                        if index != -1 and endIndexCurrentProperty < index:
                            startIndexNextProperty = index

                value = message[endIndexCurrentProperty:startIndexNextProperty]
                if startIndexNextProperty == -1:
                    value = message[endIndexCurrentProperty:]
                    
                value = CheckGrammar.cleanStartAndEnd(value).capitalize()
                taskInfo.update({currentProperty: value})

        projectID = cls.getProjectID(taskInfo[project])
        TodoistHelper.addTask(taskInfo[description], projectID)
