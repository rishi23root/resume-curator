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

