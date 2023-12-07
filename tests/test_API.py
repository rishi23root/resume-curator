import json
import re
from flask.testing import FlaskClient
from util.baseFunc import read_json_file

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
    assert isinstance(data, dict), "type of data is not dict 🚫, some errer go in detail manually"
    assert read_json_file('template.json') == data,\
            "template.json is not equal to data, please check the template.json file 🚫 or code !!"

# build all templates individually later on convert it to automated test cases
def test_create_resume_singleColumn(client: FlaskClient):
    data = {
        "data": read_json_file('template.json'),
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
    data = {
        "data": read_json_file('template.json'),
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


