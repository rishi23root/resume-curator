import json
import re

from flask.testing import FlaskClient

from util.baseFunc import read_json_file


def test_get_templates(client: FlaskClient):
    response = client.get('/templates')
    assert response.status_code == 200, "unable to get templates"
    data = json.loads(response.get_data(as_text=True))
    assert isinstance(data, list), "type of data is not list"


def test_download_template(client: FlaskClient):
    response = client.get('/download_template')
    assert response.status_code == 200, "Template not downloaded successfully 🚫"
    data = json.loads(response.get_data(as_text=True))
    # check if data is equl to template.json
    assert isinstance(data, dict), "type of data is not dict"
    assert read_json_file(
        'template.json') == data, "template.json is not equal to data, please check the template.json file 🚫 or code !!"


def test_create_resume(client: FlaskClient):
    with open('template.json') as f:
        jsonFileData = json.load(f)

    data = {
        "data": jsonFileData,
        "template": "singleColumn"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = client.post(
        '/create_resume', headers=headers, data=json.dumps(data))
    # status code is 200
    assert response.status_code == 200, "Template not downloaded successfully 🚫"

    # if the output file is pdf
    # print(response.headers)
    d = response.headers['content-disposition']
    fname = (re.findall("filename=(.+)", d)[0])
    # fname is a pdf file
    # isPdfFile = re.match(r'^.*.pdf$', fname)
    assert fname == f'{data["template"]}.pdf', "file name is not equal to template name 🚫, code Error recheck plz"

