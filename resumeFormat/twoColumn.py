import pylatex as lt
from pylatex.utils import NoEscape

from util.baseTemplate import Template
from util.htmlParser import getListItems
from util.tolatex import createLink, inBlock
from util.Exceptions import InvalidAttrException


class base(Template):
    def __init__(self):
        super().__init__()
        
    def extractData(self):
        # extract data from the json file and format it according to the template

        try:
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

            # at last masking Data
            mask = {}
            if self.jsonData.get('mask'):
                mask = self.jsonData['mask']

        except Exception as e:
            raise InvalidAttrException(" ".join(e.args),500) from e

        return {
            'userInfoContant': userInfoContant,
            'links': links,
            'experience': experience,
            'education': education,
            'skills': skills,
            'certificates': awards,
            'projects': projects,
            'mask':mask,
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
                    linkstring += createLink(
                        'mailto:' + val, val) + ' \\textbar{} \n\t'
                else:
                    linkstring += createLink(val, val) + ' \\textbar{} \n\t'
        else:
            linkstring = linkstring[:-13]

        namesection_args = [
            first, last,
            NoEscape(
                '\\vspace{-1.5em}\n'+
                '\\begin{center} ' +
                kwargs['label'] + 
                '\\end{center}\n'
                "\n\\newline"+
                '\\vspace{-0.9em}\n'+
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

    def AddEducation(self, education: dict,mask:dict):
        if not education:
            return
        # add the education section
        # print(education)
        with self.create(lt.Section(mask['education'])):
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
    
    def AddSkills(self, skills: dict,mask:dict):
        try:
            languages = skills['languages'] 
            frameworks = skills['frameworks']
            familar = skills['databases'] + skills['libraries'] + skills['technologies']
        except:
            languages = []
            frameworks = []
            familar = []
        tools = skills['tools']
        
        with self.create(lt.Section(mask['skills'])):
            if self.jsonData['basics']['label'].startswith( 'Software' ):
                self.append(NoEscape('\\subsection{Programming}\n'))
            
            under5000 = []
            under1000 = []
            for i in languages:
                if int(i['level']) > 2:
                    under5000.append(i['name'])
                else:
                    under1000.append(i['name'])
            
            self.append(lt.utils.bold(NoEscape(f'\\textbf{{{skills["mask"]["languages"].capitalize()}}} : \t')))
            
            if under5000:
                # new line
                self.append(NoEscape(' \\textbullet{} '.join(under5000)))
                self.append(NoEscape('\\vspace{0.05em}\n'))
            
            if under1000:
                self.append(NoEscape(' \\textbullet{} '.join(under1000)))
                self.append(NoEscape('\\vspace{0.05em}\n'))

            self.append(lt.NewLine())
            self.append(NoEscape('\\\\'))
            
            
            if frameworks:
                self.append(lt.utils.bold(NoEscape(f'\\textbf{{{skills["mask"]["frameworks"].capitalize()}}} : \t')))
                for index,i in enumerate(frameworks):
                    if index == 0:
                        self.append(NoEscape(i['name']))
                    else:
                        self.append(NoEscape(' \\textbullet{} ' + i['name']))
                    self.append(NoEscape('\\vspace{0.05em}\n'))
                self.append(lt.NewLine())
                self.append(NoEscape('\\\\'))
                

            # familar
            if familar:
                self.append(lt.utils.bold(NoEscape('\\textbf{Familiar} :\t')))
                for index,i in enumerate(familar):
                    if index == 0:
                        self.append(NoEscape(i['name']))
                    else:
                        self.append(NoEscape(' \\textbullet{} ' + i['name']))
                    self.append(NoEscape('\\vspace{0.05em}\n'))
                self.append(lt.NewLine())
                self.append(NoEscape('\\\\'))
                

            # tools
            if tools:
                self.append(lt.utils.bold(NoEscape(f'\\textbf{{{skills["mask"]["tools"].capitalize()}}} :\t')))
                for index,i in enumerate(tools):
                    if index == 0:
                        self.append(NoEscape(i['name']))
                    else:
                        self.append(NoEscape(' \\textbullet{} ' + i['name']))
                    self.append(NoEscape('\\vspace{0.05em}\n'))
                self.append(lt.NewLine())
                self.append(NoEscape('\\\\'))
                

            self.append(NoEscape('}%\n'))
        # pprint(skills)
        # section space
        self.append(NoEscape('\\sectionsep'))
    
    def AddCerts(self, awards: dict,mask:dict):
        if not awards:
            return
        self.append(lt.Section(mask['awards']))
        for award in awards:
            # self.append(award['title'] + '}\n'))
            # make head for the title with only first letter capital and rest small
            self.append(NoEscape('\\runsubsection{' + award['title'].capitalize() + '}\n'))
            # line seperator
            self.append(lt.NewLine())
            
            self.append(
                NoEscape('\\location{' + award['date'] + ' by ' + createLink(award['url'], award['awarder']) + '}'))
            self.append(NoEscape('\\sectionsep'))

        self.append(NoEscape('\\sectionsep'))


    # right sections
    def AddExperience(self, experience: dict,mask:dict, isTop :bool):
        if not experience:
            return
        # \runsubsection{Facebook}
        # \descript{| Software Engineer }
        # \location{Jan 2015 - Present | New York, NY}
        # \sectionsep
        self.append(NoEscape('\\section{'+mask['work']+'}'))
        self.append(NoEscape('\\vspace{2pt}'))
        
        for index,ex in enumerate(experience):
            self.append(NoEscape('\\runsubsection{' + createLink(ex['url'], ex['name']) + '}'))
            self.append(NoEscape('\\descript{\\textbar{} ' + ex['position'] + '}'))
            startingDate = str(ex['startDate'])
            endDate: str = ('Present' if ex['isWorkingHere'] else ex['endDate'])
            string = '\\location{' + startingDate + ' - ' + endDate + ' }'
            self.append(NoEscape(string))

            # # description
            if ex['summary']:
                # \vspace{\topsep} # Hacky fix for awkward extra vertical space
                # self.append(NoEscape('\\vspace{\\topsep}'))
                
                self.append(NoEscape('\\begin{tightemize}'))
                # for i in ex['summary'].split:
                # parse the list items of summeries
                if index == 0 and isTop:
                    self.append(NoEscape('\\vspace{\\topsep}'))
                    self.append(NoEscape('\\vspace{2pt}'))
                if "<li>" in ex['summary']:
                    lis = getListItems(ex['summary'])
                    for li in lis:
                        self.append(NoEscape('\\item ' + li))
                else:
                    # give a space
                    self.append(NoEscape(ex['summary']))
                    self.append(NoEscape("\\vspace{10pt}"))
                    
                self.append(NoEscape('\\end{tightemize}'))
            # # \sectionsep
            self.append(NoEscape('\\sectionsep'))
    
    def AddProjects(self, projects: dict,mask:dict, isTop :bool):
        if not projects:
            return
        self.append(NoEscape('\\section{'+mask['projects']+'}'))
        self.append(NoEscape("\\vspace{2pt}"))
        
        for index,project in enumerate(projects):
            self.append(NoEscape('\\runsubsection{' + createLink(project['url'], project['name']) + '}'))

            # # description
            if project['description']:
                # \vspace{\topsep} # Hacky fix for awkward extra vertical space
                # self.append(NoEscape("\\vspace{2pt}"))
                self.append(NoEscape('\\begin{tightemize}'))
                if index == 0 and isTop:
                    self.append(NoEscape('\\vspace{\\topsep}'))
                    self.append(NoEscape('\\vspace{2pt}'))
                if "<li>" in project['description']:
                    lis = getListItems(project['description'])
                    for li in lis:
                        self.append(NoEscape('\\item ' + li))
                else:
                    # give a space
                    self.append(NoEscape('\\vspace{\\topsep}'))
                    self.append(NoEscape(project['description']))
                    # self.append(NoEscape("\\vspace{10pt}"))
                # self.append(NoEscape(project['description']))
                self.append(NoEscape('\\end{tightemize}'))
                # self.append(NoEscape("\\vspace{6pt}"))
            
            self.append(NoEscape('\\sectionsep'))
            
            # self.append(lt.NewLine())

    def fill_document(self):
        try:
            data = self.extractData()
        except InvalidAttrException as e:
            raise Exception(f"invalid data of keys: {e.attr}",)

        # add date
        # self.append(lt.Command("lastupdated"))

        self.AddUserProfile(**data['userInfoContant'])
        
        with self.create(lt.MiniPage(width=lt.NoEscape(r"0.29\textwidth"), pos='t', content_pos='t')):
            # add the links section
            self.AddLinks(data['links'])
            # add education section
            self.AddEducation(data['education'],data['mask'])
            # add the skills section
            self.AddSkills(data['skills'],data['mask'])
            # add Awards section
            self.AddCerts(data['certificates'],data['mask'])
            
        self.append(lt.HFill())
        
        with self.create(lt.MiniPage(width=lt.NoEscape(r"0.66\textwidth"), pos='t',content_pos='t')):
            # add Experence section
            self.AddExperience(data['experience'],data['mask'],True)
            # add Projects section
            self.AddProjects(data['projects'],data['mask'],not bool(len(data['experience'])))
