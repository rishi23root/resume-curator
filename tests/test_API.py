import json
import os
import re
import uuid
from flask.testing import FlaskClient
from util.baseFunc import read_json_file
from util.constants import baseDir, outputDir

headers = {
    'Content-Type': 'application/json'
}

def test_list_templates(client: FlaskClient):
    response = client.get('/templates')
    assert response.status_code == 200, "unable to get templates"
    data = json.loads(response.get_data(as_text=True))
    # print(data)
    assert isinstance(data, list), "type of data is not list"


def test_download_template(client: FlaskClient):
    response = client.get('/download_template')
    assert response.status_code == 200, "Template not downloaded successfully 🚫"
    data = json.loads(response.get_data(as_text=True))
    # check if data is equl to template.json
    assert isinstance(data, dict), "type of data is not dict 🚫, some error go in detail manually"
    assert read_json_file('template.json') == data,\
            "template.json is not equal to data, please check the template.json file 🚫 or code !!"

# build all templates individually later on convert it to automated test cases
def test_create_resume_singleColumn(client: FlaskClient):
    with open(os.path.join(baseDir,"tests" ,'template.json'), 'r') as f:
        JSONdata = json.load(f) 

    # del JSONdata['basics']['profiles']
    data = {
        "data": JSONdata,
        "template": "singleColumn"
    }
    
    response = client.post(
        '/create_resume', headers=headers, data=json.dumps(data)
    )
    
    assert response.status_code == 200, "Template not downloaded successfully 🚫"

    # if the output file is pdf - print(response.headers)
    d = response.headers['content-disposition']
    fname = (re.findall("filename=(.+)", d)[0])
    
    # fname is a pdf file # isPdfFile = re.match(r'^.*.pdf$', fname)
    assert fname == f'{data["template"]}.pdf', "file name is not equal to template name 🚫, code Error recheck plz"

def test_create_resume_twoColumn(client: FlaskClient):
    with open(os.path.join(baseDir,"tests" ,'template.json'), 'r') as f:
        JSONdata = json.load(f) 

    # del JSONdata['basics']['profiles']
    data = {
        "data": JSONdata,
        "template": "twoColumn"
    }
    
    response = client.post(
        '/create_resume', headers=headers, data=json.dumps(data)
    )
    
    assert response.status_code == 200, "Template not downloaded successfully 🚫"

    # if the output file is pdf - print(response.headers)
    d = response.headers['content-disposition']
    fname = (re.findall("filename=(.+)", d)[0])
    
    # fname is a pdf file # isPdfFile = re.match(r'^.*.pdf$', fname)
    assert fname == f'{data["template"]}.pdf', "file name is not equal to template name 🚫, code Error recheck plz"


# format converting 
# from BYR to jsonResume
def test_convert_resume_toBYR(client: FlaskClient):
    with open(os.path.join(baseDir,"tests" ,'template.json'), 'r') as f:
        JSONdata = json.load(f) 

    # del JSONdata['basics']['profiles']
    data = {
        "data": JSONdata,
        "to2From": "BYRToJsonResume"
    }
    
    response = client.post(
        '/convert_resume', headers=headers, data=json.dumps(data)
    )
    
    assert response.status_code == 200, "Template not downloaded successfully 🚫" + response.data.decode('utf-8')

    # check if the return data is json or not
    data = json.loads(response.get_data(as_text=True))
    assert isinstance(data, dict), "type of data is not dict 🚫, some error go in detail manually"
    
    # check if data have fields like - interests, languages, 
    assert "interests" in data, "interests field is not present in data"
    assert "languages" in data, "languages field is not present in data"
    # print()
    # print(data)

# from jsonResume to BYR
def test_convert_resume_toJR(client: FlaskClient):
    with open(os.path.join(baseDir,"tests" ,'jr.json'), 'r') as f:
        JSONdata = json.load(f) 

    # del JSONdata['basics']['profiles']
    data = {
        "data": JSONdata,
        "to2From": "jsonResumeToBYR"
    }
    
    response = client.post(
        '/convert_resume', headers=headers, data=json.dumps(data)
    )
    
    # print()
    # print(response.data.decode('utf-8'))
    
    assert response.status_code == 200, "Template not downloaded successfully 🚫" + response.data.decode('utf-8')

    # check if the return data is json or not
    data = json.loads(response.get_data(as_text=True))
    assert isinstance(data, dict), "type of data is not dict 🚫, some error go in detail manually"
    
    # check if data should not have fields like - interests, languages
    assert "interests" not in data, "interests field is present in data"
    assert "languages" not in data, "languages field is present in data" 
    
    # and must have fields like - 
    for i in ["skills", "awards", "basics", "work", "education", "projects", "mask"]:
        assert i in data, f"{i} field is not present in data"
        # assert "languages" not in data, "languages field is present in data" 
    

def test_getJpgPreview(client: FlaskClient):
    data = {
        "file": open(os.path.join(outputDir ,'singleColumn.pdf'), 'rb')
    }
    
    response = client.post(
        '/getJpgPreview', data=data
    )
    
    assert response.status_code == 200, "images not downloaded successfully 🚫" + response.data.decode('utf-8')        
    if response.status_code == 200: 
        assert isinstance(response.json, list), "type of data is not list 🚫, some error go in detail manually"
    else:
        assert False, "error with return status code for the api"