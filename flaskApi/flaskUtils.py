# flask base api to generate resume form the data recieved from the frontend
# tasks
# 0. recieve the data from the frontend
# a. authenticate user
# b. get the json data from the frontend
# 1. create resume and save in some folder
# 2. send the resume to the frontend in byte format and delete the file from the folder

import os
import uuid
from pathlib import Path

from util.constants import baseDir
from util.utils import getTemplates, read_json_file


def athenticateUser(request):
    return True


def generateResume(data: dict, templateName: str) -> Path or None:
    # file name to save the resume
    # return full path of the resume with the file name
    fileName = str(uuid.uuid4()) + '.pdf'

    # get the template and call the function
    templateCall = getTemplates(templateName)
    if templateCall is not None:
        return templateCall(fileName, data)
    else:
        return None


def varifyData(data: dict) -> bool:
    # varify the data
    if data is None:
        return False, "data is None"
    # read the json file and varify the data
    templateData = read_json_file(os.path.join(baseDir, 'template.json'))
    for field in templateData.keys():
        # level1
        if field not in data.keys():
            return False, field

        if isinstance(templateData[field], dict):
            for i in templateData[field].keys():
                # level2
                if i not in data[field].keys():
                    return False, '.'.join([field, i])
        else:
            # list
            # select the first element from the list
            example = templateData[field][0]
            for eachElementInList in data[field]:
                for eachField in example.keys():
                    if eachField not in eachElementInList.keys():
                        return False, '.'.join([field, eachField])
    return True, ""
