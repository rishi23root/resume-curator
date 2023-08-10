from pylatex.utils import NoEscape
import pylatex as lt
from util.htmlParser import getListItems
from util.utils import read_json_file, createResume
from util.tolatex import createLink
from util.constants import resumeJsonFile, buildDir
import os


class MyDocument(lt.Document):
    def __init__(self):
        super().__init__(documentclass='resumecustom',
                         page_numbers=False,
                         document_options={},
                         fontenc=None, # type: ignore
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
        if self.jsonData is None:
            self.jsonData = read_json_file(resumeJsonFile)
            
        userInfoContant = {
            'name': self.jsonData['basics']['name'],
            'email': self.jsonData['basics']['email'],
            'phone': self.jsonData['basics']['phone'],
            'website': self.jsonData['basics']['url'],
            'address': ", ".join([i for i in [self.jsonData['basics']['location']['city'], self.jsonData['basics']['location']['postalCode']] if i != '']),
            'label': self.jsonData['basics']['label'],
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

    # header
    def AddUserProfile(self, **kwargs):
        # name: str, email: str, phone: str, website: str, address: str
        # name
        # name = "Rahul Kumar"
        try:
            first, last = kwargs['name'].split(" ")
        except:
            first = kwargs['name']
            last = ''
        # profile links
        linkstring = ''
        for key, val in kwargs.items():
            if key not in ['name', 'label', 'links']:
                if key in ['phone', 'address']:
                    linkstring += val + ' \\textbar{} \n\t'
                elif key == 'email':
                    linkstring += createLink('mailto:' +
                                             val, val) + ' \\textbar{} \n\t'
                else:
                    linkstring += createLink(val, val) + ' \\textbar{} \n\t'
        else:
            linkstring = linkstring[:-13]

        # adding social links
        socialLinks = []
        for link in kwargs['links']:
            if not link['url'] or not link['username']:
                continue

            network = link['network'].capitalize()
            url = link['url']

            # add to social links
            socialLinks.append(
                lt.utils.bold(NoEscape(f'\\href{{{url}}}{{{network}}}'))
            )

        namesection_args = [
            first, last,
            NoEscape(
                '\n\t' + kwargs['label'] +
                '\n\n\t\\urlstyle{same}\n\t' +
                linkstring + 
                "\n\\newline"+
                '\\vspace{-0.7em}\n'+
                '\\begin{center} ' +
                " \\textbar{} ".join(socialLinks) +
                '\\end{center}\n'
            )
        ]
        nameSection = lt.Command(
            "namesectionsinglelayout", arguments=namesection_args)
        self.append(nameSection)

    # left sections

    def AddEducation(self, education: dict):
        self.append(NoEscape('\\fieldsection{Education}{\n'))
        for edu in education:
            institution = edu['institution']
            study_type = edu['studyType']
            area = edu['area']
            start_date = edu['startDate']
            end_date = edu['endDate']
            score = edu['score']
            isStudyingHere = edu['isStudyingHere']
            studytime = f'{start_date} - {end_date if not isStudyingHere else "Present"}'

            # \vspace{0.5em}
            self.append(NoEscape(f'\\textbf{{{institution}}} \\hfill {area}\n'))
            self.append(NoEscape('\\newline\n'))
            self.append(NoEscape(f'{study_type} \\hfill {studytime}\n'))
            self.append(NoEscape('\\vspace{0.5em}\n'))
            self.append(NoEscape('\\newline\n'))

        self.append(NoEscape('}%\n'))

    def AddSkills(self, skills: dict):
        languages = skills['languages'] + skills['frameworks']
        familar = skills['databases'] + skills['libraries'] + skills['technologies']
        tools = skills['tools']
        
        self.append(NoEscape('\\fieldsection{Skills}{\n'))
        # add space
        self.append(NoEscape('\\vspace{0.5em}\n'))
        
        under5000 = []
        under1000 = []
        for i in languages:
            if int(i['level']) > 60:
                under5000.append(i['name'])
            else:
                under1000.append(i['name'])
        
        # languages
        if under5000:
            self.append(lt.utils.bold(NoEscape('\\textbf{Over 5000 lines:}')))
            # new line
            self.append(lt.NewLine())
            self.append(NoEscape(' \\textbullet{} '.join(under5000)))
            self.append(NoEscape('\\vspace{0.2em}\n'))
            self.append(lt.NewLine())
        
        if under1000:
            self.append(lt.utils.bold(NoEscape('\\textbf{Over 5000 lines:}')))
            # new line
            self.append(lt.NewLine())
            self.append(NoEscape(' \\textbullet{} '.join(under1000)))
            self.append(NoEscape('\\vspace{0.2em}\n'))
            self.append(lt.NewLine())

        # if len(under5000) < len(languages):
        #     self.append(lt.utils.bold(NoEscape('\\textbf{Over 1000 lines:}\t')))
        #     self.append(lt.NewLine())
        #     self.append(NoEscape(' \\textbullet{} '.join([i['name'] for i in languages if i not in under5000])))
        #     self.append(NoEscape('\\vspace{0.2em}\n'))
        #     self.append(lt.NewLine())

        # familar
        if familar:
            self.append(lt.utils.bold(NoEscape('\\textbf{Familiar:}\n\t')))
            self.append(lt.NewLine())
            for i in familar:
                self.append(NoEscape(' \\textbullet{} ' + i['name']))
            self.append(NoEscape('\\vspace{0.2em}\n'))
            self.append(lt.NewLine())

        # tools
        if tools:
            self.append(lt.utils.bold(NoEscape('\\textbf{Tools:}\n\t')))
            self.append(lt.NewLine())
            for i in tools:
                self.append(NoEscape(' \\textbullet{} ' + i['name']))
            self.append(lt.NewLine())
            self.append(NoEscape('\\vspace{0.2em}\n'))


        

        self.append(NoEscape('}%\n'))

    def AddCerts(self, awards: dict):
        self.append(NoEscape('\\fieldsection{certificates}{\n'))
        for award in awards:
            title = award['title']
            url = award['url']            
            nameWithUrl = f'{title}'+' - ' + createLink(url, award['awarder'])
            self.append(NoEscape(f'\\textbf{{{nameWithUrl}}} \\hfill {award["date"]}'))
            self.append(NoEscape('\\vspace{0.5em}\n'))
            self.append(lt.NewLine())

        self.append(NoEscape('}%\n'))

    def AddExperience(self, experience: dict):
        self.append(NoEscape('\\fieldsection{Experience}{\n'))
        for ex in experience:
            name = ex['name']
            # \\textbar{}
            position = ex['position']
            startingDate = str(ex['startDate'])
            endDate: str = (
                'Present' if ex['isWorkingHere'] else ex['endDate'])
            worktime = f'{startingDate} - {endDate}'

            nameWithPossition = f'{name}'+' \\textbar{} ' + f'{position}'

            # \vspace{0.5em}
            self.append(
                NoEscape(f'\\textbf{{{nameWithPossition}}} \\hfill {worktime}'))
            # self.append(NoEscape('\\newline\n'))
            # self.append(NoEscape(f'{study_type} \hfill {studytime}\n'))
            if ex['summary']:
                #         # \vspace{\topsep} # Hacky fix for awkward extra vertical space
                #         self.append(NoEscape('\\vspace{\\topsep}'))
                self.append(NoEscape('\\begin{tightemize}'))
                if "<li>" in ex['summary']:
                    lis = getListItems(ex['summary'])
                    for li in lis:
                        self.append(NoEscape('\\item ' + li))
                else:
                    # give a space
                    self.append(NoEscape("\\vspace{10pt}"))
                    self.append(NoEscape(ex['summary']))
                    # self.append(NoEscape('\\item ' + "line1"))
                self.append(NoEscape('\\end{tightemize}'))
                pass
            
            self.append(NoEscape('\\vspace{0.5em}\n'))

        self.append(NoEscape('}%\n'))
        self.append(NoEscape('\\vspace{0.5em}\n'))

    def AddProjects(self, projects: dict):
        self.append(NoEscape('\\fieldsection{projects}{\n'))
        for project in projects:
            name = project['name']
            url = project['url']
            languages = project['languages']
            
            nameWithUrl = f'{name}'+' \\textbar{} ' + createLink(url, "Link")
            
            self.append(NoEscape(f'\\textbf{{{nameWithUrl}}} \\hfill {languages}'))
            # self.append(NoEscape('\\newline'))
            # self.append(NoEscape(f'{study_type} \hfill {studytime}\n'))
            # self.append(NoEscape('\\newline\n'))
            # # description
            if project['discription']:
                # \vspace{\topsep} # Hacky fix for awkward extra vertical space
                # self.append(NoEscape('\\vspace{\\topsep}'))
                self.append(NoEscape('\\begin{tightemize}'))
                self.append(NoEscape("\\vspace{10pt}"))
                self.append(NoEscape(project['discription']))
                self.append(NoEscape('\\end{tightemize}'))
            
            self.append(NoEscape('\\vspace{0.5em}\n'))

        self.append(NoEscape('}%\n'))

    def fill_document(self):
        data = self.extractData()

        # add date
        self.append(lt.Command("lastupdated"))

        self.AddUserProfile(**data['userInfoContant'],links=data['links'])
        self.append(lt.NewLine())
        self.append(lt.NewLine())
        
        # add education section
        self.AddEducation(data['education'])
        # # add Experence section
        self.AddExperience(data['experience'])
        # # add the skills section
        self.AddSkills(data['skills'])
        # # add Projects section
        self.AddProjects(data['projects'])
        # # add Awards section
        self.AddCerts(data['certificates'])

def runner(filename: str = 'resume.pdf',jsonData: dict = None): # type: ignore
    name = filename.split('.')[0]
    doc = MyDocument()
    if jsonData:
        doc.jsonData = jsonData

    # Call function to add text
    doc.fill_document()

    # # doc.generate_pdf(clean_tex=False)
    doc.generate_tex(filepath=os.path.join(buildDir, name))

    return createResume(filename)
