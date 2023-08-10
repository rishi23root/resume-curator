import subprocess
import os
from util.runSystem import runSystemCommad


templateFolderName = 'resumeFormat'
resumeJsonFileName = 'template.json'
builderDirName = 'builder'
outputDirName = 'output'

baseDir = os.getcwd()

templateDir = os.path.join(baseDir, templateFolderName)
buildDir = os.path.join(baseDir, builderDirName)

resumeJsonFile = os.path.join(baseDir, resumeJsonFileName)

# outputDir
outputDir = os.path.join(baseDir, outputDirName)

# print(templateDir)
# print(resumeJsonFile)

# if out dir doesn't exist create one
if os.path.isdir(outputDir) == False:
    os.mkdir(outputDir)

# set default liveonfly path


def tivetextPaht():
    # check if the texliveonfly is installed or not
    # in home or default logical path
    try:
        # command = "which pdflatex | xargs dirname"
        # a = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()  # type: ignore

        # if a == '. . .' or a == '':
        defalttexlivePath = '/texlive/2023/bin/x86_64-linux'
        homePath = subprocess.Popen(
            "echo $HOME", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()  # type: ignore
        a = (homePath+defalttexlivePath)
        # elif not a:
        #     raise Exception("empty", a)
    except Exception as e:
        raise Exception("texlive not found in the system", e)

    print(a)
    return a


textlivePath = tivetextPaht()

# add the texlive path to the $PATH
runSystemCommad(f'export PATH=$PATH:{textlivePath}')
runSystemCommad(f'source ~/.bashrc')
