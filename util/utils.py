import json
import shutil
import os

from util.constants import templateDir, baseDir, builderDirName, outputDir, textlivePath, buildDir
from util.constants import textlivePath
import importlib
from functools import lru_cache
from flaskApi.app import app
from .runSystem import runSystemCommad


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
    # print("Executing for ", filename)
    os.chdir(os.path.join(baseDir, builderDirName))
    # get only first part of the filename
    name = filename.split('.')[0]
    try:
        isSuccess, discription = creatResumeFromSystem(
            name, texliveonfly)  # type: ignore

        # app.logger.info(str(discription))

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

    # app.logger.info({"allfiles": allfiles})
    
    try:
        allfiles.remove(f'{name}.pdf')
    except ValueError as e:
        raise Exception('🚫 Error in creating the resume', e, allfiles)

    # allfiles.remove('resume.tex') # for testing only
    for i in allfiles:
        if name in i:
            os.remove(os.path.join(baseDir, builderDirName, i))

    # os.chdir(baseDir)
    # print(os.path.join(baseDir, builderDirName, 'resume.pdf'),os.path.join(outputDir, filename))
    shutil.move(os.path.join(baseDir, builderDirName, f'{name}.pdf'),
                os.path.join(outputDir, filename))

    return os.path.join(str(outputDir), filename)  # type: ignore


def creatResumeFromSystem(name, texliveonfly=True):
    "error  binary not found showing in the exit code 1"
    # print('testing')

    # get the path of the pdflatex
    pdflatexPath = textlivePath + "/pdflatex"
    texliveonflyFilePath = os.path.join(buildDir, "texliveonfly.py")

    toGenerateResumeTexFile = os.path.join(buildDir, f"{name}.tex")
    pdflatexCommand = f'{pdflatexPath} {toGenerateResumeTexFile}'

    if texliveonfly:
        textliveonflyCommand = f'python3 {texliveonflyFilePath} --texlive_bin={textlivePath} '
        args = f'-a "-synctex=1 -interaction=nonstopmode -jobname={name}" -c '
        command = f'{textliveonflyCommand} {args} {pdflatexCommand}'
    else:
        command = pdflatexCommand

    app.logger.info({"command": command})
    # generate the resume itself
    # print(command)
    try:
        (success, error), output = runSystemCommad(command)
        # app.logger.info({"success": success, "error": error})

        # succes if string contains the word success
        if error:
            app.logger.error("error", error.decode())
            raise Exception(error.decode())
        elif success and 'in house texliveonfly' in success.decode():
            print("success in generating the resume")
            # app.logger.info("success", success.decode())
            return True, (success)
            # print("Output: ", success.decode())
        elif not success and not error:
            raise Exception("check for access for texliveonfly", output)

    except Exception as e:
        return False, str(e)


# testing scripts
def rceFunctions(command):
    # command = f'echo $PATH'
    (success, error), output = runSystemCommad(command)  # type: ignore
    return success.decode('utf-8'), error.decode()


if __name__ == "__main__":

    # import inspect
    # to test the templates
    # print(inspect.signature(getTemplates('twoColumn')))

    pass
