import subprocess
import os

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
    command = "echo $(dirname $(which texliveonfly))"
    defalttexlivePath = '/texlive/2023/bin/x86_64-linux'
    a = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()

    if a:
        print("current texliveonfly path is :", a)
        return a
    else:
        homePath = subprocess.Popen(
            "echo $HOME", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip()
        print("current texliveonfly path is :", homePath+defalttexlivePath)
        return homePath+defalttexlivePath

textlivePath = tivetextPaht()
