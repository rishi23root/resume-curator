from pylatex.utils import NoEscape
import pylatex as lt
from util.htmlParser import getListItems
from util.utils import read_json_file, createResume
from util.tolatex import createLink
from constants import resumeJsonFile, buildDir
import os


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
            'label': jsonData['basics']['label'],
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
                linkstring + '\n\n' +
                '\n\t' + " \\textbar{} ".join(socialLinks) +
                '\n'
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
            self.append(NoEscape(f'\\textbf{{{institution}}} \hfill {area}\n'))
            self.append(NoEscape('\\newline\n'))
            self.append(NoEscape(f'{study_type} \hfill {studytime}\n'))
            self.append(NoEscape('\\vspace{0.5em}\n'))
            self.append(NoEscape('\\newline\n'))

        self.append(NoEscape('}%\n'))

    def AddSkills(self, skills: dict):
        languages = skills['languages'] + skills['frameworks']
        familar = skills['databases'] + \
            skills['libraries'] + skills['technologies']
        tools = skills['tools']
        
        self.append(NoEscape('\\fieldsection{Skills}{\n'))
        # add space
        self.append(NoEscape('\\vspace{0.5em}\n'))
        
        # rfsdhflksd
        under5000 = []
        for i in languages:
            if int(i['level']) > 60:
                under5000.append(i['name'])
        # languages
        if under5000:
            self.append(lt.utils.bold(NoEscape('\\textbf{Over 5000 lines:}')))
            # new line
            self.append(lt.NewLine())
            self.append(NoEscape(' \\textbullet{} '.join(under5000)))
            self.append(NoEscape('\\vspace{0.2em}\n'))
            self.append(lt.NewLine())

        if len(under5000) < len(languages):
            self.append(lt.utils.bold(NoEscape('\\textbf{Over 1000 lines:}\t')))
            self.append(lt.NewLine())
            self.append(NoEscape(' \\textbullet{} '.join([i['name'] for i in languages if i not in under5000])))
            self.append(NoEscape('\\vspace{0.2em}\n'))
            self.append(lt.NewLine())

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


        # with self.create(lt.Section('Skill')):
        #     self.append(NoEscape('\\subsection{Programming}'))

        #     under5000 = []
        #     for i in languages:
        #         if int(i['level']) > 60:
        #             under5000.append(i['name'])
        #     # languages
        #     if under5000:
        #         self.append(lt.utils.bold(
        #             NoEscape('\\location{Over 5000 lines:}')))
        #         self.append(NoEscape(' \\textbullet{} '.join(under5000)))
        #     if len(under5000) < len(languages):
        #         self.append(lt.utils.bold(
        #             NoEscape('\\location{Over 1000 lines:}')))
        #         self.append(NoEscape(' \\textbullet{} '.join(
        #             [i['name'] for i in languages if i not in under5000]
        #         )))
        #     self.append(lt.NewLine())

        #     # familar
        #     if familar:
        #         self.append(lt.utils.bold(NoEscape('\\location{Familiar:}\n')))
        #         for i in familar:
        #             self.append(NoEscape(' \\textbullet{} ' + i['name']))
        #         self.append(lt.NewLine())

        #     # tools
        #     if tools:
        #         self.append(lt.utils.bold(NoEscape('\\location{Tools:}\n')))
        #         for i in tools:
        #             self.append(NoEscape(' \\textbullet{} ' + i['name']))

        # # pprint(skills)
        # # section space
        # self.append(NoEscape('\\sectionsep'))

    def AddCerts(self, awards: dict):
        self.append(NoEscape('\\fieldsection{projects}{\n'))
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
                NoEscape(f'\\textbf{{{nameWithPossition}}} \hfill {worktime}'))
            # self.append(NoEscape('\\newline\n'))
            # self.append(NoEscape(f'{study_type} \hfill {studytime}\n'))
            if ex['summary']:
                #         # \vspace{\topsep} # Hacky fix for awkward extra vertical space
                #         self.append(NoEscape('\\vspace{\\topsep}'))
                self.append(NoEscape('\\begin{tightemize}'))
                lis = getListItems(ex['summary'])
                for li in lis:
                    self.append(NoEscape('\\item ' + li))
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
            
            self.append(NoEscape(f'\\textbf{{{nameWithUrl}}} \hfill {languages}'))
            # self.append(NoEscape('\\newline'))
            # self.append(NoEscape(f'{study_type} \hfill {studytime}\n'))
            # self.append(NoEscape('\\newline\n'))
            # # description
            if project['discription']:
                # \vspace{\topsep} # Hacky fix for awkward extra vertical space
                # self.append(NoEscape('\\vspace{\\topsep}'))
                self.append(NoEscape('\\begin{tightemize}'))
                self.append(NoEscape('\\item ' + project['discription']))
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

def runner(filename: str = 'resume.pdf'):
    doc = MyDocument()

    # Call function to add text
    doc.fill_document()

    # # doc.generate_pdf(clean_tex=False)
    doc.generate_tex(filepath=os.path.join(buildDir, 'resume'))

    createResume(filename)
