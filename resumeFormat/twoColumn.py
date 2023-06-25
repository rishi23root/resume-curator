# handel all the logic for the two column resume format
# create resume.tex file from the template.json file

from pylatex.utils import italic, NoEscape
import pylatex as lt
from util.htmlParser import getListItems
from util.utils import read_json_file, createResume
from util.tolatex import createLink, inBlock
from constants import resumeJsonFile, buildDir
import os


from pprint import pprint   

class MyDocument(lt.Document):
    def __init__(self):
        super().__init__(documentclass='resumecustom',
                         page_numbers=False,
                         document_options={},
                         fontenc=None,
                         lmodern=False,
                         textcomp=False,
                         microtype=False)

        # self.preamble.append(lt.Command('title', 'Rishi23root resume builder'))
        # self.preamble.append(lt.Command('author', 'Rishi23root'))
        # self.preamble.append(lt.Command('date', NoEscape(r'\today')))
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
            'address': ", ".join([i for i in [jsonData['basics']['location']['city'], jsonData['basics']['location']['postalCode']] if i != '']),
        }
        links = jsonData['basics']['profiles']
        experience = jsonData['work']
        education = jsonData['education']
        skills = jsonData['skills']
        projects = jsonData['projects']
        awards = jsonData['awards']

        return {
            'userInfoContant': userInfoContant,
            'links': links,
            'experience': experience,
            'education': education,
            'skills': skills,
            'certificates': awards,
            'projects': projects
        }

    # header
    def AddUserProfile(self, **kwargs):
        # name: str, email: str, phone: str, website: str, address: str
        # name
        # name = "Rahul Kumar"
        first, last = kwargs['name'].split(" ")

        # profile links
        linkstring = ''
        for key, val in kwargs.items():
            if key != 'name':
                if key in ['phone', 'address']:
                    linkstring += val + ' \\textbar{} \n\t'
                elif key == 'email':
                    linkstring += createLink('mailto:' +
                                             val, val) + ' \\textbar{} \n\t'
                else:
                    linkstring += createLink(val, val) + ' \\textbar{} \n\t'
        else:
            linkstring = linkstring[:-13]

        namesection_args = [
            first, last,
            NoEscape(
                '\n\t\\urlstyle{same}\n\t' +
                linkstring +
                '\n'
            )
        ]
        nameSection = lt.Command("namesection", arguments=namesection_args)
        self.append(nameSection)

    # left sections
    def AddLinks(self, links: dict):
        # add the links section
        with self.create(lt.Section('Links')):
            for link in links:
                if not link['url'] or not link['username']:
                    continue
                
                network = link['network'].capitalize()
                username = link['username']

                self.append(f"{network}:// ")
                self.append(NoEscape(createLink( link['url'], lt.utils.bold(username))))
                self.append("\n")

    def AddEducation(self, education: dict):
        # add the education section
        # print(education)
        with self.create(lt.Section('Education')):
            for edu in education:
                institution = edu['institution']
                study_type = edu['studyType']
                area = edu['area']
                start_date = edu['startDate']
                end_date = edu['endDate']
                score = edu['score']
                isStudyingHere = edu['isStudyingHere']

                # Create the education entry
                with self.create(lt.Subsection(title=institution)):
                    self.append(NoEscape(inBlock('descript', f'{study_type} in {area}')))

                    self.append(NoEscape(inBlock('descript', f'{start_date} | {end_date if not isStudyingHere else "Present"}') + '\n'))

                    if score:
                        self.append('Score: ' + NoEscape(score))
                    self.append(NoEscape('\\sectionsep'))
                    
            # self.append(NoEscape('\\sectionsep'))
    
    def AddSkills(self, skills: dict):
        languages = skills['languages'] + skills['frameworks']
        familar = skills['databases'] + skills['libraries'] + skills['technologies']
        tools = skills['tools']
        with self.create(lt.Section('Skill')):
            self.append(NoEscape('\\subsection{Programming}'))
            
            under5000 = []
            for i in languages:
                if int(i['level']) > 60:
                    under5000.append(i['name'])
            # languages  
            if under5000:
                self.append(lt.utils.bold(NoEscape('\\location{Over 5000 lines:}')))
                self.append(NoEscape(' \\textbullet{} '.join(under5000)))
            if len(under5000) < len(languages):
                self.append(lt.utils.bold(NoEscape('\\location{Over 1000 lines:}')))
                self.append(NoEscape(' \\textbullet{} '.join(
                    [i['name'] for i in languages if i not in under5000]
                )))
            self.append(lt.NewLine())

            # familar
            if familar:
                self.append(lt.utils.bold(NoEscape('\\location{Familiar:}\n')))
                for i in familar:
                    self.append(NoEscape(' \\textbullet{} ' + i['name']))
                self.append(lt.NewLine())

            # tools
            if tools:
                self.append(lt.utils.bold(NoEscape('\\location{Tools:}\n')))
                for i in tools:
                    self.append(NoEscape(' \\textbullet{} ' + i['name']))

        # pprint(skills)
        # section space
        self.append(NoEscape('\\sectionsep'))
    
    def AddCerts(self, awards: dict):
        self.append(lt.Section('Certificates'))
        for award in awards:
            self.append(NoEscape('\\subsection{Programming}'))
            self.append(NoEscape('\\subsection{' + award['title'] + '}\n'))
            self.append(
                NoEscape('\\location{' + award['date'] + ' by ' + award['awarder'] + '}'))
            self.append(NoEscape('\\sectionsep'))

        self.append(NoEscape('\\sectionsep'))


    
    # right sections
    def AddExperience(self, experience: dict):
        # \runsubsection{Facebook}
        # \descript{| Software Engineer }
        # \location{Jan 2015 - Present | New York, NY}
        # \sectionsep
        self.append(NoEscape('\\section{Experience}'))
        for ex in experience:
            self.append(NoEscape('\\runsubsection{' + ex['name'] + '}'))
            self.append(NoEscape('\\descript{\\textbar{} ' + ex['position'] + '}'))
            startingDate = str(ex['startDate'])
            endDate: str = ('Present' if ex['isWorkingHere'] else ex['endDate'])
            string = '\\location{' + startingDate + ' - ' + endDate + ' }'
            self.append(NoEscape(string))

            # # description
            if ex['summary']:
                # \vspace{\topsep} # Hacky fix for awkward extra vertical space
                self.append(NoEscape('\\vspace{\\topsep}'))
                self.append(NoEscape('\\begin{tightemize}'))
                # for i in ex['summary'].split:
                # parse the list items of summeries
                lis = getListItems(ex['summary'])
                for li in lis:
                    self.append(NoEscape('\\item ' + li))
                self.append(NoEscape('\\end{tightemize}'))
            # # \sectionsep
            self.append(NoEscape('\\sectionsep'))
        
    
    def AddProjects(self, projects: dict):
        print(projects)
        
        self.append(NoEscape('\\section{Projects}'))
        
        for project in projects:
            self.append(NoEscape('\\runsubsection{' + project['name'] + '}'))

            self.append(
                NoEscape(' \\textbar{} ' + createLink(project['url'],"Link")+'\n')
            )
            
            
            # project['languages']

            # # description
            if project['discription']:
                # \vspace{\topsep} # Hacky fix for awkward extra vertical space
                self.append(NoEscape('\\vspace{\\topsep}'))
                # self.append(NoEscape('\\begin{tightemize}'))
                # # self.append(project['discription'])
                # self.append(NoEscape('\\end{tightemize}'))
                self.append(NoEscape('\\sectionsep'))
            
            # \sectionsep

    def fill_document(self):
        data = self.extractData()

        # add date
        self.append(lt.Command("lastupdated"))

        self.AddUserProfile(**data['userInfoContant'])
        with self.create(lt.MiniPage(width=lt.NoEscape(r"0.31\textwidth"), pos='t', content_pos='t')):
            # add the links section
            self.AddLinks(data['links'])
            # add education section
            self.AddEducation(data['education'])
            # add the skills section
            self.AddSkills(data['skills'])
            # add Awards section
            self.AddCerts(data['certificates'])
            
        self.append(lt.HFill())

        with self.create(lt.MiniPage(width=lt.NoEscape(r"0.66\textwidth"), pos='t',content_pos='t')):
            # add Experence section
            self.AddExperience(data['experience'])
            # add Projects section
            self.AddProjects(data['projects'])

        # add sub mini pages for other data like education, experience, skills etc


def runner(filename: str = 'resume.pdf'):
    doc = MyDocument()

    # Call function to add text
    doc.fill_document()

    # # doc.generate_pdf(clean_tex=False)
    doc.generate_tex(filepath=os.path.join(buildDir, 'resume'))

    createResume(filename)
