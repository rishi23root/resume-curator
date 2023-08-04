import json
import shutil
from pathlib import Path
import os

from util.constants import templateDir, baseDir, builderDirName, outputDir, textlivePath, buildDir
import subprocess
import importlib
from functools import lru_cache
from flaskApi.app import app


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
        raise Exception('Error in reading json file, check the json format')


def createResume(filename: str, isSilent: bool = True, texliveonfly=True) :
    os.chdir(os.path.join(baseDir, builderDirName))
    command = f'python3 {os.path.join(buildDir,"texliveonfly.py")+" -c" if texliveonfly else "" } pdflatex {os.path.join(buildDir,"resume.tex")}'

    try:
        runSystemCommad(command)
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
        raise Exception('Error in creating the resume, check the logs', e)

    # allfiles.remove('resume.tex') # for testing only
    for i in allfiles:
        os.remove(os.path.join(baseDir, builderDirName, i))

    # os.chdir(baseDir)
    # print(os.path.join(baseDir, builderDirName, 'resume.pdf'),os.path.join(outputDir, filename))
    shutil.move(os.path.join(baseDir, builderDirName, 'resume.pdf'),
                os.path.join(outputDir, filename))

    return os.path.join(str(outputDir), filename)  # type: ignore


def runSystemCommad(command: str):
    "error  binary not found showing in the exit code 1"
    # print('testing')
    try:
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        success, error = output.communicate()  # get the output and error
        # print exit code
        
        # succes if string contains the word success
        if success and 'in house texliveonfly' in success.decode():
            print("success")
            # print("Output: ", success.decode())
        elif error or 'in house texliveonfly' not in success.decode() :
            raise Exception("unable to create the resume, check the logs",error.decode())
        elif not success and not error:
            raise Exception("check for access for texliveonfly", output)
    
    except Exception as e:
        # print('Error : ', e)
        # app.logger.error(e)
        raise Exception(e)

    # raise Exception('jksdfhsdhjkfsdfjkh fsdjklhfadksjflk ;')


# testing scripts
def testPdflatexAccess(isSilent: bool = True, texliveonfly=True):
    command = f'python3 {os.path.join(buildDir,"texliveonfly.py")+" -c" if texliveonfly else "" } pdflatex {os.path.join(buildDir,"resume.tex")}'
    # command = f'{os.path.join(textlivePath,"texliveonfly")+" -c" if texliveonfly else "" } pdflatex resume.tex '
    # print(command)
    # output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read().decode('utf-8').strip()  # type: ignore
    output = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    success, error = output.communicate()  # get the output and error
    if success:
        if not isSilent:
            print("success")
            print("Output: ", success.decode())
    elif error:
        print(error.decode())
        raise Exception("unable to create the resume, check the logs")
    elif not success and not error:
        raise Exception("check for access for texliveonfly", output)


if __name__ == "__main__":

    # import inspect
    # to test the templates
    # print(inspect.signature(getTemplates('twoColumn')))

    pass
