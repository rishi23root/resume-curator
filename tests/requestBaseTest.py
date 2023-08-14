import requests
import json
import re

baseUrl = 'http://localhost:5000/'

baseUrl = 'https://api.buildyourresume.online/'

print('testing', baseUrl)


def createResume(templateName="singleColumn"):
    url = baseUrl + 'create_resume'

    # Example JSON data
    with open('template.json') as f:
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


if __name__ == '__main__':
    listTemplates()
    downloadTemplate()
    createResume()
    createResume('twoColumn')

    # os.remove('template.json')
