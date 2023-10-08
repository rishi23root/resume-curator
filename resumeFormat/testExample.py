# for understing of how to implement of a new temaplaet 

import pylatex as lt
from pylatex.utils import NoEscape

from util.baseTemplate import Template
from util.htmlParser import getListItems
from util.tolatex import createLink, inBlock

# fill_document is compulsory to have, beacuse used in execution it will not give you error but no results will be found on not providing it because it overwrites an existing function

class base(Template):
    def __init__(self):
        super().__init__()
        
    def extractData(self):
        # extract data from the json file and format it according to the template
                    
        userInfoContant = {
            'name': self.jsonData['basics']['name'],
            'email': self.jsonData['basics']['email'],
            'phone': self.jsonData['basics']['phone'],
            'website': self.jsonData['basics']['url'],
            'address': ", ".join([i for i in [self.jsonData['basics']['location']['city'], self.jsonData['basics']['location']['postalCode']] if i != '']),
        }
        links = self.jsonData['basics']['profiles']
        experience = self.jsonData['work']
        education = self.jsonData['education']
        skills = self.jsonData['skills']
        projects = self.jsonData['projects']
        awards = self.jsonData['awards']

        return {
            'userInfoContant': userInfoContant,
            'links': links,
            'experience': experience,
            'education': education,
            'skills': skills,
            'certificates': awards,
            'projects': projects
        }

    
    # exmaple of different section to use or add do whatever you want
    # header
    def AddUserProfile(self, **kwargs):
        pass

    # left sections
    def AddLinks(self, links: dict):
        pass

    def AddEducation(self, education: dict):
        pass
        
    def AddSkills(self, skills: dict):
        pass
    
    def AddCerts(self, awards: dict):
        pass


    # right sections
    def AddExperience(self, experience: dict):
        pass
    
    def AddProjects(self, projects: dict):
        pass

    def fill_document(self):
        pass
