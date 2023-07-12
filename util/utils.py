import json
import shutil
from pathlib import Path
import os
from constants import baseDir, builderDirName, outputDir


def read_json_file(file_path: str):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise Exception('Error in reading json file, check the json format')

def createResume(filename: str) -> Path:
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
    allfiles.remove('resumecustom.cls')
    allfiles.remove('resume.pdf')
    
    # allfiles.remove('resume.tex') # for testing only
    for i in allfiles:
        os.remove(os.path.join(baseDir, builderDirName, i))

    # os.chdir(baseDir)
    # print(os.path.join(baseDir, builderDirName, 'resume.pdf'),os.path.join(outputDir, filename))
    shutil.move(os.path.join(baseDir, builderDirName, 'resume.pdf'),
                os.path.join(outputDir, filename))
    
    return os.path.join(outputDir, filename)


if __name__ == "__main__":
    # print(read_resume_josn())
    # print(extract_template(1))
    # print(createSection('hello', 'world'))
    pass
