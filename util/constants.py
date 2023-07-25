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

texlivePath = '/texlive/2023/bin/x86_64-linux'
# get the base path of the texliveonfly
# a= os.system(, shell=True)
# print(a)
command = "echo $(dirname $(which texliveonfly))"
# subprocess.run(["ls", "-l"])
a = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
print(a)