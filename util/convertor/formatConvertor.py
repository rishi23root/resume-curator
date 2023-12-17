# Desc: convert jsonResume format to our template and vice versa
from bs4 import BeautifulSoup
from pprint import pprint

profileData = {
    "network": "",
    "username": "",
    "url": ""
}

ourMustHaveFields = {
    "basics":{
        "name": "",
        "label": "",
        "email": "",
        "image": "",
        "phone": "",
        "url": "",
        "summary": "",
        "location": {
            "address": "",
            "postalCode": "",
            "city": "",
            "countryCode": "",
            "region": ""
        },
        "profiles": [
        ]
    },
    "work":[],
    "education":[],
    "skills":{
        "frameworks": [],
        "technologies": [],
        "libraries": [],
        "databases": [],
        "tools": [],
        "mask":{
            "core": "core",
            "interests": "interests",
            "languages": "languages",
            "frameworks": "frameworks",
            "technologies": "technologies",
            "libraries": "libraries",
            "databases": "databases",
            "tools": "tools"    
        }
    },
    "projects":[],
    "awards":[],
    "mask": {
        "basics": "basics",
        "skills": "skills",
        "education": "education",
        "work": "work",
        "projects": "projects",
        "awards": "certificates"
    }
}

# to jsonResume format to Our template
def JsonResumeToOurTemplate(data):
    # Parse the JSON string into a Python dictionary
    resume_data = data

    # Your custom format
    personal_format = ourMustHaveFields.copy()
    personal_format['basics'] = resume_data["basics"]
    
    
    # work
    for index,worke in enumerate(resume_data["work"]):        
        worke["id"] = str(index+1)
        worke["isWorkingHere"] = True if worke["endDate"] else False
        worke['summary'] = "<ul>" + " ".join(f"<li>{i}</li>" for i in worke['highlights']) + "</ul>"
        del worke['highlights']
        worke["years"] = ""
        personal_format['work'].append(worke)
    
    # print(resume_data["education"])
    for index,education in enumerate(resume_data["education"]):        
        education["id"] = str(index+1)
        education["isStudyingHere"] = True if education["endDate"] else False
        personal_format['education'].append(education)
        
    
    # personal_format['projects'] = resume_data["projects"]
    for index,projects in enumerate(resume_data["projects"]):        
        projects["id"] = str(index+1)
        projects["languages"] = ""
        projects["description"] = ""
        del projects['highlights']
        del projects['endDate']
        personal_format['projects'].append(projects)
    
    # personal_format['skills'] = resume_data["skills"]
    personal_format['skills']["core"] = resume_data["skills"]
    personal_format['skills']["interests"]= [{
        "name" : interests["name"],
        
    } for interests in resume_data["interests"]]  
    personal_format['skills']["languages"] = [{
        "name" : lang["language"],
        "level" : 0
    } for lang in resume_data["languages"]]  
    
    # awards and certificates
    for index,awards in enumerate(resume_data["awards"]):        
        awards["id"] = str(index+1)
        # if key is not present in dict then it will return None
        awards["url"] = awards.get("url", "")    
        personal_format['awards'].append(awards)
        
    for index,awards in enumerate(resume_data["certificates"]):        
        awards["id"] = str(index+1)
        awards['title'] = awards['name']
        del awards['name']
        awards['awarder'] = awards['issuer']
        awards['summary'] = ""
        # if key is not present in dict then it will return None
        awards["url"] = awards.get("url", "")
        
        personal_format['awards'].append(awards)

    return personal_format



# from Our template to jsonResume format
def OurTemplateToJsonResume(data):
    # Parse the data from your template
    personal_format = data

    # jsonResume format
    resume_data = {
        "basics": personal_format["basics"],
        "work": [],
        "education": [],
        "projects": [],
        "skills": personal_format["skills"]["core"],
        "interests": [{
            "name": interest["name"],
            "keywords": []
            } for interest in personal_format["skills"]["interests"]],
        "languages": [{"language":lang["name"],'fluency':""} for lang in personal_format["skills"]["languages"]],
        "awards": [],
        "certificates": []
    }

    # work experience
    for work in personal_format['work']:
        work_data = work.copy()
        work_data['endDate'] = '' if work_data['isWorkingHere'] else work_data.pop('endDate')
        del work_data['isWorkingHere']
        work_data['highlights'] = [highlight.text for highlight in BeautifulSoup(work_data['summary'], 'html.parser').find_all('li')]
        del work_data['summary']
        del work_data['years']
        resume_data['work'].append(work_data)

    # education
    for education in personal_format['education']:
        education_data = education.copy()
        education_data['endDate'] = '' if education_data['isStudyingHere'] else education_data.pop('endDate')
        education_data['courses'] = [] 
        del education_data['isStudyingHere']
        resume_data['education'].append(education_data)

    # projects
    for project in personal_format['projects']:
        project_data = project.copy()
        project_data['endDate'] = ''
        project_data['startDate'] = ''
        project_data['highlights'] = [highlight.text for highlight in BeautifulSoup(project_data['description'], 'html.parser').find_all('li')]
        resume_data['projects'].append(project_data)

    # awards and certificates
    for award in personal_format['awards']:
        award_data = award.copy()
        if award_data.get('name'):
            award_data['title'] = award_data.pop('name')
        del award_data['id']
        resume_data['awards'].append(award_data)

    return resume_data



if __name__ == "__main__":
    # read jr.json in dir
    # openresume = open("./util/convertor/jr.json", "r")
    # data = openresume.read()
    # jsonDATA = json.loads(data)
    # jsonDATA = JsonResumeToOurTemplate(jsonDATA)
    # out = varifyData(jsonDATA)
    # print(out)
    
    # templateData = read_json_file(os.path.join(baseDir, 'template.json'))
    # out = OurTemplateToJsonResume(templateData)
    # pprint(out['skills'])
    pass