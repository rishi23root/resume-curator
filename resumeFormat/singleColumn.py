import pylatex as lt
from pylatex.utils import NoEscape

from util.baseTemplate import Template
from util.htmlParser import getListItems
from util.tolatex import createLink
from util.Exceptions import InvalidAttrException

class base(Template):
    '''
    this template is highly inspired from hackerrank clasic template but not a copy :)
    '''
    def __init__(self):
        super().__init__()
    
    def extractData(self):
        """Extract data and varify if all the required can be extracted or not if not then rise error accordingly"""
        
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
    def AddEducation(self, education: dict,mask:dict):
        self.append(NoEscape('\\fieldsection{'+mask['education']+'}{\n'))
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
            self.append(NoEscape(f'{study_type} '))
            if score:
                self.append(NoEscape('\\textbar{} ')) 
                self.append(f' Score: {score}')
                
            self.append(NoEscape(f'\\hfill {studytime}\n'))
            
            self.append(NoEscape('\\vspace{0.5em}\n'))
            self.append(NoEscape('\\newline\n'))

        self.append(NoEscape('}%\n'))

    def AddSkills(self, skills: dict,mask:dict):
        languages = skills['languages'] + skills['frameworks']
        familar = skills['databases'] + skills['libraries'] + skills['technologies']
        tools = skills['tools']
        
        self.append(NoEscape('\\fieldsection{'+mask['skills']+'}{\n'))
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

    def AddCerts(self, awards: dict,mask:dict):
        self.append(NoEscape('\\fieldsection{'+mask['awards']+'}{\n'))
        for award in awards:
            title = award['title']
            url = award['url']            
            nameWithUrl = f'{title}'+' - ' + createLink(url, award['awarder'])
            self.append(NoEscape(f'\\textbf{{{nameWithUrl}}} \\hfill {award["date"]}'))
            self.append(NoEscape('\\vspace{0.5em}\n'))
            self.append(lt.NewLine())

        self.append(NoEscape('}%\n'))

    def AddExperience(self, experience: dict,mask:dict):
        self.append(NoEscape('\\fieldsection{'+mask['work']+'}{\n'))
        for ex in experience:
            name = ex['name']
            position = ex['position']
            url = ex['url']
            startingDate = str(ex['startDate'])
            endDate: str = (
                'Present' if ex['isWorkingHere'] else ex['endDate'])
            worktime = f'{startingDate} - {endDate}'

            nameWithPossition = f'{createLink(url, name)}'+' \\textbar{} ' + f'{position}'

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

    def AddProjects(self, projects: dict,mask:dict):
        self.append(NoEscape('\\fieldsection{'+mask['projects']+'}{\n'))
        for project in projects:
            name = project['name']
            url = project['url']
            languages = project['languages']
            
            nameWithUrl = createLink(url, name)
            # nameWithUrl = f'{name}'+' \\textbar{} ' + createLink(url, "Link")
            
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
        try:
            data = self.extractData()
        except InvalidAttrException as e:
            # print(e.message)
            raise Exception(f"invalid data of keys: {e.attr}",)

        # add date
        # self.append(lt.Command("lastupdated"))

        self.AddUserProfile(**data['userInfoContant'],links=data['links'])
        self.append(lt.NewLine())
        self.append(lt.NewLine())
        
        # add education section
        self.AddEducation(data['education'],data['mask'])
        # # add Experence section
        self.AddExperience(data['experience'],data['mask'])
        # # add the skills section
        self.AddSkills(data['skills'],data['mask'])
        # # add Projects section
        self.AddProjects(data['projects'],data['mask'])
        # # add Awards section
        self.AddCerts(data['certificates'],data['mask'])
