'''Main Todoist Class'''
import json

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
    """Summary of class here

    Attributes:
        notionTopQueueTask (str): telegram instance
        apiAsync (str): todoist async api retrieved from a specific token
        api (str): todoist api retrieved from a specific token

    Methods:
        getProjectsAsync(): 
        getProjects(): 
        getTasksAsync(): 
        getTasks(): 
        addTask(): 
    """
    notionTopQueueTask = None
    apiAsync = TodoistAPIAsync(Todoist.TOKEN)
    api = TodoistAPI(Todoist.TOKEN)

    #---------------------------------------------------------------

    @classmethod
    async def getProjectsAsync(cls):
        """ -- """
        return cls.apiAsync.get_projects()

    #---------------------------------------------------------------

    @classmethod
    def getProjects(cls):
        """ -- """
        return cls.api.get_projects

    #---------------------------------------------------------------

    @classmethod
    async def getTasksAsync(cls):
        """ -- """
        return cls.apiAsync.get_tasks()

    #---------------------------------------------------------------

    @classmethod
    def getTasks(cls):
        """ -- """
        return cls.api.get_tasks()
    
    #---------------------------------------------------------------

    @classmethod
    def addTask(cls, title, projectID, content='', due=None):
        """ -- """
        try:
            if content is None:
                content = ''
            task = TodoistHelper.api.add_task(content=title, project_id=projectID, description=content, due_string=due)
            Utils.sendMessage(f"[ADD TASK: - Content: {title} - ProjectID: {projectID}]")
        except (RuntimeError, ValueError, IndexError) as error:
            Utils.sendMessage(f"[ERROR: {error} - Content: {title} - ProjectID: {projectID}]")


###################################
#|||||||||||||| API ||||||||||||||#
###################################
class TodoistApi:
    """Summary of class here

    Attributes:
        
    Methods:
        getProjectTasks(): 
        getProjectNames(): 
        getProjectID(): 
        manageTodoistTask(): 
    """

    #---------------------------------------------------------------

    @classmethod
    def getProjectTasks(cls, projectID=None):
        """ -- """
        return [task for task in TodoistHelper.api.get_tasks() if task.project_id == projectID]

    #---------------------------------------------------------------

    @classmethod
    def getProjectNames(cls):
        """ -- """
        return [p.name for project in TodoistHelper.api.get_projects() for p in project]

    #---------------------------------------------------------------

    @classmethod
    def getProjectID(cls, projectName):
        """ -- """
        if not projectName:
            return None

        projectList = list(TodoistHelper.api.get_projects())
        for project in projectList:
            for p in project:
                if projectName.lower() == p.name.lower():
                    return p.id

        return None

    #---------------------------------------------------------------

    @classmethod
    def manageTodoistTask(cls, taskInfo, links):
        """ -- """
        # URLs
        title = taskInfo[Todoist.TITLE]
        description = taskInfo[Todoist.DESCRIPTION]

        if links is not None:
            for hiperlink in links:
                url = links[hiperlink]
                title = title.replace(hiperlink, f"[{hiperlink}]({url})")

                if description is not None:
                    description = description.replace(hiperlink, f"[{hiperlink}]({url})")

        # Extract dictionary data
        title = CheckGrammar.cleanStartAndEnd(title)

        if description is not None:
            description = CheckGrammar.cleanStartAndEnd(description)

        date = taskInfo[Todoist.DATE]

        project = TodoistApi.getProjectID(taskInfo[Todoist.PROJECT])

        TodoistHelper.addTask(title, project, description, date)

    #---------------------------------------------------------------
