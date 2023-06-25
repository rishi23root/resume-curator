# handel all the logic for the two column resume format
# create resume.tex file from the template.json file

from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape
import pylatex as lt

from util.utils import read_json_file, saveTEXFile, createResume
from util.tolatex import createLink
from constants import resumeJsonFile, buildDir
import os


class MyDocument(Document):
    def __init__(self):
        super().__init__(documentclass='resumecustom',
                         page_numbers=False,
                         document_options={},
                         fontenc=None,
                         lmodern=False,
                         textcomp=False,
                         microtype=False)

        # self.preamble.append(Command('title', 'Awesome Title'))
        # self.preamble.append(Command('author', 'Anonymous author'))
        # self.preamble.append(Command('date', NoEscape(r'\today')))
        # self.append(NoEscape(r'\maketitle'))

        # setup for base data
        self.change_document_style("fancy")
        self.remove(lt.Command("pagestyle", arguments=["empty"]))
        self.remove(lt.Command("normalsize"))
        self.packages.remove(lt.Package("inputenc", options=["utf8"]))
        # adding imp packages to start the document
        self.packages.append(lt.Package('fancyhdr'))
        self.append(lt.Command("fancyhf", arguments=[""]))

    def extractData(self):
        # extract data from the json file and format it according to the template
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

    def AddUserProfile(self, *args, **kwargs):
        # name: str, email: str, phone: str, website: str, objective: str
        # name
        # name = "Rahul Kumar"
        first, last = kwargs['name'].split(" ")

        
        # profile links
        linkstring = ''
        for key,val in kwargs.items():
            if key not in ['name','objective']:
                if key == 'phone':
                    linkstring += val + ' \\textbar{} \n\t'
                else:
                    linkstring += createLink(val, val) + '\\textbar{} \n\t'
        else:
            linkstring = linkstring[:-13]

        namesection_args = [
            first, last,
            NoEscape(
                '\n\t\\urlstyle{same}\n\t'+
                linkstring+
                '\n\t\\newline\n\t'+
                kwargs['objective'] +'\n'              
            )
        ]
        nameSection = lt.Command("namesection", arguments=namesection_args)
        self.append(nameSection)

    def fill_document(self):
        data = self.extractData()

        # add date
        self.append(lt.Command("lastupdated"))
        print(data['userInfoContant'])
        self.AddUserProfile(**data['userInfoContant'])


# userInfoWrapper = latexBlock(
#     'namesection', '{'+f'{name.split(" ")[0]}'+'}'+'{'+f'{name.split(" ")[1]}'+'}{', '}')

# userInfoData = fr"""
# {inBlock('urlstyle',"{same}")}

# {createLink(email,email)} |
# {phone} |
# {createLink(website,website)}
# \newline
# {objective}
# """

# texCode += f'''
# {sectionNameString}
# {userInfoWrapper(userInfoData)}
# '''

# retu`rn texCode


def runner(filename: str = 'resume.pdf'):
    doc = MyDocument()

    # Call function to add text
    doc.fill_document()

    # # doc.generate_pdf(clean_tex=False)
    doc.generate_tex(filepath=os.path.join(buildDir, 'resume'))

    createResume(filename)
