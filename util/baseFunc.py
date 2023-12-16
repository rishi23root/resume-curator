import importlib
import json
import os
from functools import lru_cache
from pprint import pprint

from util.constants import templateDir

# Can update it to some other reasonable way later 
notRealTemaplate= 'test'

@lru_cache()
def listTemplates():
    """get list of templates can be use"""
    dirContent = os.listdir(templateDir)
    # remove all the directories
    templateNames =  [eachFile.split('.')[0] for eachFile in dirContent if os.path.isfile(
        os.path.join(templateDir, eachFile))] # type: ignore
    # filter out templates name with example or testing
    templateNames = list(filter(lambda templateName: notRealTemaplate not in templateName , templateNames))
    return templateNames

@lru_cache()
def extractFuncCallsForTemplate():
    """return a dict of all runner functions for the tempalates"""
    onlyTemplates = listTemplates()
    # create dict with all the templates
    return {
        each: importlib.import_module(f'resumeFormat.{each}').base.run for each in onlyTemplates
    }

@lru_cache()
def useTemplates(templateName: str) -> callable or None:  # type: ignore
    """extract the template to run"""
    functionCallForEach= extractFuncCallsForTemplate()
    if templateName not in functionCallForEach: return None
    return functionCallForEach[templateName]

@lru_cache()
def read_json_file(file_path: str):
    """read the json file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise Exception('🚫 Error in reading json file, check the json format')


# local logger in case not running in server mode
class logger:
    def error(self, x):
        print("[ERROR] : ",end='')
        pprint(x)

    def info(self, x):
        print("[INFO] : ",end='')
        pprint(x)


class app:
    logger = logger()
