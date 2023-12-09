import requests
import json
import re
import os 


# baseUrl = 'https://api.buildyourresume.online/'
baseUrl = 'http://localhost:5000/'
folderPath =  os.path.join(os.getcwd(),"tests" )

print('Testing for :', baseUrl, '\nin', folderPath,end="\n\n")

def listTemplates():
    url = baseUrl + 'templates'

    # Make the GET request
    response = requests.get(url)

    # Handle the response
    if response.status_code == 200:
        print('Templates:', response.json())
    else:
        print('🚫 Error:', response.text)


def downloadTemplate():
    url = baseUrl + 'download_template'

    # Make the GET request
    response = requests.get(url)

    # Handle the response
    if response.status_code == 200:
        # Save the response content (resume) to a file
        d = response.headers['content-disposition']
        fname = (re.findall("filename=(.+)", d)[0])
        with open(fname, 'wb') as f:
            f.write(response.content)
        print('Template downloaded successfully.')
    else:
        print('🚫 Error:', response.text)


def createResume(templateName="singleColumn"):
    url = baseUrl + 'create_resume'

    # Example JSON data
    with open(os.path.join(folderPath ,'template.json'), 'r') as f:
        data = json.load(f)

    data = {
        "data": data,
        "template": templateName
    }
    headers = {
        'Content-Type': 'application/json'
    }

    # Make the POST request
    # print(data.keys())
    response = requests.post(url, data=json.dumps(data), headers=headers)
    # Handle the response
    if response.status_code == 200:
        # Save the response content (resume) to a file
        d = response.headers['content-disposition']
        fname = (re.findall("filename=(.+)", d)[0])
        with open(fname, 'wb') as f:
            f.write(response.content)
        print('Resume downloaded successfully.')
    else:
        print(response.status_code)
        print('🚫 Error:', response.text)
        print(response.headers)
        # print(response.json())

# convert format from BYR to jsonResume
def convertResumeToBYR():
    url = baseUrl + 'convert_resume'

    # Example JSON data
    with open(os.path.join(folderPath ,'template.json'), 'r') as f:
        JsonData = json.load(f)

    data = {
        "data": JsonData,
        "to2From": "BYRToJsonResume"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Handle the response
    if response.status_code == 200:
        # print all the keys in the response
        print('Resume downloaded successfully.')
        print(response.json().keys())
    else:
        print(response.status_code)
        print('🚫 Error:', response.text)
        print(response.headers)
        
# convert format from jsonResume to BYR
def convertResumeToJsonResume():
    url = baseUrl + 'convert_resume'

    # Example JSON data
    with open(os.path.join(folderPath ,'jr.json'), 'r') as f:
        JsonData = json.load(f)

    data = {
        "data": JsonData,
        "to2From": "jsonResumeToBYR"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Handle the response
    if response.status_code == 200:
        # print all the keys in the response
        print('Resume downloaded successfully.')
        print(response.json().keys())
    else:
        print(response.status_code)
        print('🚫 Error:', response.text)
        print(response.headers)


if __name__ == '__main__':
    listTemplates()
    downloadTemplate()
    createResume()
    createResume('twoColumn')
    convertResumeToBYR()
    convertResumeToJsonResume()

    # os.remove('template.json')
