import json
import shutil
from pathlib import Path
import os
from util.constants import templateDir, baseDir, builderDirName, outputDir

import importlib
from functools import lru_cache



@lru_cache()
# get list of templates
def listTemplates():
    dirContent = os.listdir(templateDir)
    # remove all the directories
    return [eachFile.split('.')[0] for eachFile in dirContent if os.path.isfile(
        os.path.join(templateDir, eachFile))]

@lru_cache()
# extract the template to run
def getTemplates(templateName:str) -> callable or None:
    onlyTemplates = listTemplates()
    # crate dict with all the templates
    functionCallForEach = {each: importlib.import_module(f'resumeFormat.{each}').runner for each in onlyTemplates}
    if templateName not in functionCallForEach:
        return None
    return functionCallForEach[templateName]


def read_json_file(file_path: str):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise Exception('Error in reading json file, check the json format')

def createResume(filename: str,isSilent:bool=False) -> Path:
    os.chdir(os.path.join(baseDir, builderDirName))
    if not isSilent:
        os.system(
            f'texliveonfly -c pdflatex resume.tex'
        )
    else:
        # final version of the resume
        os.system(
            f'texliveonfly -c pdflatex resume.tex | tee /proc/sys/vm/drop_caches >/dev/null 2>&1'
        )

    # remove the other files other then resume-custom.cls
    allfiles = os.listdir(os.path.join(baseDir, builderDirName))
    print(allfiles)
    allfiles.remove('resumecustom.cls')
    try:
        allfiles.remove('resume.pdf')
    except ValueError as e:
        raise Exception('Error in creating the resume, check the logs',e)
    
    # allfiles.remove('resume.tex') # for testing only
    for i in allfiles:
        os.remove(os.path.join(baseDir, builderDirName, i))

    # os.chdir(baseDir)
    # print(os.path.join(baseDir, builderDirName, 'resume.pdf'),os.path.join(outputDir, filename))
    shutil.move(os.path.join(baseDir, builderDirName, 'resume.pdf'),
                os.path.join(outputDir, filename))
    
    return os.path.join(outputDir, filename)


if __name__ == "__main__":
    
    
    # import inspect
    # to test the templates
    # print(inspect.signature(getTemplates('twoColumn')))

    pass
