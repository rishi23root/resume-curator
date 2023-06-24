# handel all the logic for the two column resume format
# create resume.tex file from the template.json file

from util.utils import read_json_file, saveTEXFile, createResume, removeEmptySpace
from constants import resumeJsonFile, outputDir
from util.tolatex import createLink, createSection, latexBlock, inBlock
import os


# tasks
# 1. function to create user profile section  - name, email, phone, website, objective


# todo functions 
# 1. to create the each indivisual sections  
# 2. function to extract data and format it according to the template
# 3. 


# extract data from the json file and format it according to the template
def extractTeamplateData():
    jsonData = read_json_file(resumeJsonFile)
    userInfoContant = {
        'name': jsonData['basics']['name'],
        'email': jsonData['basics']['email'],
        'phone': jsonData['basics']['phone'],
        'website': jsonData['basics']['url'],
        'objective': jsonData['basics']['objective']
    }
    links = jsonData['basics']['profiles']
    experience = jsonData['work']
    education = jsonData['education']
    skills = jsonData['skills']
    # projects = jsonData['projects']
    # awards = jsonData['awards']
    return {
        'userInfoContant': userInfoContant,
        'links': links,
        'experience': experience,
        'education': education,
        'skills': skills
    }


def createUserInfo(name: str, email: str, phone: str, website: str, objective: str):
    texCode = ""
    sectionNameString = r'''
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %
    %     TITLE NAME
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    '''
    # adding the user info
    userInfoWrapper = latexBlock(
        'namesection', '{'+f'{name.split(" ")[0]}'+'}'+'{'+f'{name.split(" ")[1]}'+'}{', '}')
    userInfoData = fr"""
    {inBlock('urlstyle',"{same}")}

    {createLink(email,email)} |
    {phone} | 
    {createLink(website,website)}
    \newline
    {objective}
    """

    texCode += f'''
    {sectionNameString}
    {userInfoWrapper(userInfoData)}
    '''

    return texCode


def runner(filename: str = 'resume.pdf' ):
    data = extractTeamplateData()
    userInfoContant = data['userInfoContant']
    
    # resume.tex
    texFileData = r'''
    \documentclass[]{resume-custom}
    \usepackage{fancyhdr}

    \pagestyle{fancy}
    \fancyhf{}

    \begin{document}

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %
    %     LAST UPDATED DATE
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    \lastupdated

    '''

    
    # persuing the template structure here 
    
    # adding the user info
    texFileData += createUserInfo(**userInfoContant)
    
    # columns 1 
    

    texFileData += r'\end{document}'
    
    texFileData = removeEmptySpace(texFileData)
    saveTEXFile(texFileData)
    
    createResume(filename)
    
    # os.system(f'open {os.path.join(outputDir,filename)}')

    # print(links)


# runner()