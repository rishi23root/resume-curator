import os

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from util.constants import baseDir
from util.utils import listTemplates

from .flaskUtils import athenticateUser, generateResume, varifyData
from urllib.parse import urlsplit

app = Flask(__name__)
CORS(app)

@app.route('/templates', methods=['GET'])
def list_template():
    return jsonify(listTemplates())


@app.route('/download_template', methods=['GET'])
def download_template():
    template_path = os.path.join(baseDir, 'template.json')

    if not os.path.isfile(template_path):
        return "Template file not found", 404

    return send_file(template_path, as_attachment=True)


@app.route('/create_resume', methods=['POST'])
def create_resume():
    # 0. Receive the data from the frontend
    print(request.headers)
    print(request.method)
    
    # muybe texliveonfly is not able to be accessed by the python env try with out

    # a. Authenticate user (implement your authentication logic here)
    if not athenticateUser(request):
        return "Authentication failed!", 401

    print(request.headers)
    
    # b. Get the JSON data from the frontend
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({'error': 'Invalid content type. Expected JSON.'}), 400

    try:
        # get data from the request
        jsonData = request.get_json()
        data = jsonData['data']
        templateName = jsonData['template']

        Varifed, error = varifyData(data)
        if not Varifed:
            raise KeyError(error)

        # 1. Create resume and save in some folder and return the path of the resume
        resume_output_path = generateResume(data, templateName=templateName)
        print("generated file path", resume_output_path)
        # 2. Send the resume to the frontend in byte format and delete the file from the folder

        try:
            return send_file(resume_output_path, download_name=f'{templateName}.pdf', as_attachment=True)
        finally:
            os.remove(resume_output_path)

    except KeyError as e:
        return jsonify({'error': f'Invalid data, missing key {e}'}), 422

    except Exception as e:
        # print(e.with_traceback())
        # get only the site url
        url_parts = urlsplit(request.base_url)

        base_url = url_parts.scheme + "://" + url_parts.netloc
        print(base_url)
        return jsonify({'error': f'Invalid content template, Download template from here {base_url}/download_template'}), 422


@app.route('/create_resume_bulk', methods=['POST'])
def create_resume_bulk():
    # 0. recieve the data as list
    # 1. get the json data from the frontend
    # a. create resume and save in some folder
    # b. send the resume to the frontend in byte format and delete the file from the folder
    return "under development", 200
