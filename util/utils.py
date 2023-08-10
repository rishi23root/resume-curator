import json
import shutil
from pathlib import Path
import os

from util.constants import templateDir, baseDir, builderDirName, outputDir, textlivePath, buildDir
from util.constants import textlivePath
import subprocess
import importlib
from functools import lru_cache
from flaskApi.app import app


def runSystemCommad(command: str):
    """run the system command and return the output, error and execution object """
    output = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output.communicate(), output


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
    functionCallForEach = {each: importlib.import_module(
        f'resumeFormat.{each}').runner for each in onlyTemplates}
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


def createResume(filename: str, isSilent: bool = True, texliveonfly=True):
    os.chdir(os.path.join(baseDir, builderDirName))
    try:
        isSuccess, discription = creatRumeFromSystem(
            texliveonfly)  # type: ignore
        if not isSuccess:
            raise Exception(discription)

    except Exception as e:
        app.logger.error(e)
        return None

    # remove the other files other then resume-custom.cls
    allfiles = os.listdir(os.path.join(baseDir, builderDirName))
    # not these files
    allfiles.remove('resumecustom.cls')
    allfiles.remove('texliveonfly.py')

    # allfiles.remove('test.py')

    try:
        allfiles.remove('resume.pdf')
    except ValueError as e:
        raise Exception('🚫 Error in creating the resume', e, allfiles)

    # allfiles.remove('resume.tex') # for testing only
    for i in allfiles:
        os.remove(os.path.join(baseDir, builderDirName, i))

    # os.chdir(baseDir)
    # print(os.path.join(baseDir, builderDirName, 'resume.pdf'),os.path.join(outputDir, filename))
    shutil.move(os.path.join(baseDir, builderDirName, 'resume.pdf'),
                os.path.join(outputDir, filename))

    return os.path.join(str(outputDir), filename)  # type: ignore


def creatRumeFromSystem(texliveonfly=True):
    "error  binary not found showing in the exit code 1"
    # print('testing')

    # get the path of the pdflatex
    pdflatexPath = textlivePath + "/pdflatex"
    command = f'python3 {os.path.join(buildDir,"texliveonfly.py")+" -c" if texliveonfly else "" } {pdflatexPath} {os.path.join(buildDir,"resume.tex")}'

    # generate the resume itself
    try:
        (success, error), output = runSystemCommad(command)
        # get the output and error
        # print exit code

        # succes if string contains the word success
        if success and 'in house texliveonfly' in success.decode():
            print("success")
            return True, (success)
            # print("Output: ", success.decode())
        elif error or 'in house texliveonfly' not in success.decode():
            raise Exception(
                "unable to create the resume, check the logs", error.decode())
        elif not success and not error:
            raise Exception("check for access for texliveonfly", output)

    except Exception as e:
        return False, str(e)


# testing scripts
def testPdflatexAccess(command):
    # command = f'echo $PATH'
    (success, error), output = runSystemCommad(command)  # type: ignore
    return success.decode('utf-8'), error.decode()


if __name__ == "__main__":

    # import inspect
    # to test the templates
    # print(inspect.signature(getTemplates('twoColumn')))

    pass
