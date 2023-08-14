import importlib
import json
import os
from functools import lru_cache
from pprint import pprint

from util.constants import templateDir


@lru_cache()
# get list of templates
def listTemplates():
    dirContent = os.listdir(templateDir)
    # remove all the directories
    return [eachFile.split('.')[0] for eachFile in dirContent if os.path.isfile(
        os.path.join(templateDir, eachFile))]


@lru_cache()
# extract the template to run
def getTemplates(templateName: str) -> callable or None:  # type: ignore
    onlyTemplates = listTemplates()
    # crate dict with all the templates
    functionCallForEach = {
        each: importlib.import_module(f'resumeFormat.{each}').runner   for each in onlyTemplates
        }
    if templateName not in functionCallForEach:
        return None
    return functionCallForEach[templateName]


def read_json_file(file_path: str):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise Exception('🚫 Error in reading json file, check the json format')


# local logger
class logger:
    def error(self, x):
        print("[ERROR] : ",end='')
        pprint(x)

    def info(self, x):
        print("[INFO] : ",end='')
        pprint(x)


class app:
    logger = logger()
