import json
import shutil
import os
from constants import templateDir, resumeJsonFile, baseDir, builderDirName, outputDir

# tasks
# 0. json data decorator to raise error on format error
# 1. function to read the file template.json
# 2. function to extract templates
# 3. function to chage dir and execute the command and then copy the file to the current directory
# 4. run the code to run the resume builder and then copy the file to the current directory


def read_json_file(file_path: str):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise Exception('Error in reading json file, check the json format')


def read_resume_josn():
    return read_json_file(resumeJsonFile)

# get list of templates
def get_templates():
    return os.listdir(templateDir)


def extract_template(template_id: int):
    # get the list
    allTemplates = get_templates()
    if 0 < template_id-1 > len(allTemplates):
        raise Exception('template id is not valid')

    template = allTemplates[template_id-1]
    print(template)
    return read_json_file(os.path.join(templateDir, template))

def removeEmptySpace(data: str):
    # remove trailing and leading spaces
    data.strip()
    
    # remove empty space from the starting of each line
    data = '\n'.join([i.lstrip() for i in data.split('\n')])
    return data

def saveTEXFile(texFileData: str):
    os.chdir(os.path.join(baseDir, builderDirName))
    with open('resume.tex', 'w') as f:
        f.write(texFileData)


def createResume(filename: str):
    os.chdir(os.path.join(baseDir, builderDirName))
    os.system(
        f'pdflatex resume.tex'
    )
    
    # final version of the resume
    # os.system(
    #     f'pdflatex resume.tex | tee /proc/sys/vm/drop_caches >/dev/null 2>&1'
    # )
    # cp resume.pdf ../
    # remove the other files other then resume-custom.cls
    allfiles = os.listdir(os.path.join(baseDir, builderDirName))
    # print(allfiles)
    allfiles.remove('resume-custom.cls')
    allfiles.remove('resume.pdf')
    
    allfiles.remove('resume.tex') # for testing only
    for i in allfiles:
        os.remove(os.path.join(baseDir, builderDirName, i))

    # os.chdir(baseDir)
    # print(os.path.join(baseDir, builderDirName, 'resume.pdf'),os.path.join(outputDir, filename))
    shutil.move(os.path.join(baseDir, builderDirName, 'resume.pdf'),
                os.path.join(outputDir, filename))


if __name__ == "__main__":
    # print(read_resume_josn())
    # print(extract_template(1))
    # print(createSection('hello', 'world'))
    pass
