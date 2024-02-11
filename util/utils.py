import os
import shutil

from util.constants import (baseDir, buildDir, builderDirName, outputDir,
                            textlivePath)

from .runSystem import runSystemCommad

try :
    # if not called from the main.py
    from flaskApi.app import app
except Exception as e:
    from .baseFunc import app

def createResume(filename: str, isSilent: bool = True, texliveonfly=True):
    # print("Executing for ", filename)
    os.chdir(os.path.join(baseDir, builderDirName))
    # get only first part of the filename
    name = filename.split('.')[0]
    try:
        isSuccess, description = creatResumeFromSystem(
            name, texliveonfly)  # type: ignore

        # app.logger.info(str(description))

        if not isSuccess:
            raise Exception(description)

    except Exception as e:
        # print(e)
        try:
            app.logger.error(e)
        except:
            pass
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
        textliveonflyCommand = f'/bin/python3 {texliveonflyFilePath} --texlive_bin={textlivePath} '
        args = f'-a "-synctex=1 -interaction=nonstopmode -jobname={name}" -c '
        command = f'{textliveonflyCommand} {args} {pdflatexCommand}'
    else:
        command = pdflatexCommand
        
    # app.logger.error("is textliveonly :" + str(texliveonfly))
    # app.logger.error(command)
    # app.logger.info({"command": command})
    # generate the resume itself
    try:
        (success, error), output = runSystemCommad(command)
        # print(error.decode())
        # app.logger.info({"success": success, "error": error})
        # print("Output: ", output)

        # succes if string contains the word success
        if error and 'UnicodeDecodeError' not in error.decode():
            print(app)
            try:
                app.logger.error(error.decode())  # Fix: Removed the extra argument "error"
            except:
                raise Exception(error.decode())
        elif success and 'Unable to start' in success.decode():
            raise Exception("check for access for texliveonfly", success.decode())
        elif success and 'in house texliveonfly' in success.decode():
            print("success in generating the resume")
            # app.logger.info("success", success.decode())
            return True, success.decode()
            # Fix: Removed the unnecessary parentheses around "success"
            # print("Output: ", success.decode())
        elif not success and not error:
            raise Exception("check for access for texliveonfly", output)
    except UnicodeDecodeError as e:
        return True, success.decode()
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
    # print(inspect.signature(useTemplates('twoColumn')))

    pass
