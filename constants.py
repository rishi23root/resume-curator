import os 

templateFolderName = 'resumeFormat'
resumeJsonFileName = 'template.json'
builderDirName = 'builder'
outputDirName = 'output'

templateDir = os.path.join(os.path.dirname(__file__), templateFolderName)

resumeJsonFile = os.path.join(os.path.dirname(__file__), resumeJsonFileName)

baseDir = os.path.dirname(__file__) ## no use of this
# print(templateDir)
# print(resumeJsonFile)

# outputDir
outputDir = os.path.join(os.path.dirname(__file__), outputDirName)

# if out dir doesn't exist create one
if os.path.isdir(outputDir) == False:
    os.mkdir(outputDir)