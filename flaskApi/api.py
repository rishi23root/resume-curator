import os
from urllib.parse import urlsplit

from flask import jsonify, request, send_file
from flask_cors import CORS

from util.baseFunc import listTemplates  # circular import issue
from util.constants import baseDir,outputDir
from util.utils import rceFunctions
from util.pdfImage import convertToPageImage

from .app import app
from .flaskUtils import athenticateUser, generateResume, varifyData

######################################################3
# for testing only remove in production
if app.debug:
    @app.route('/test', methods=['GET'])
    def test():
        # extract prams from the request
        command = request.args.get('command', default='id', type=str)
        # checkif the texliveonfly is working
        # check if pdflatex is accssible
        # check the access of the pylatex package
        
        systemReturn = rceFunctions(command)
        return jsonify({'return': systemReturn}) if len(systemReturn) else "Test passed" # type: ignore

######################################################3


@app.route('/templates', methods=['GET'])
def list_template():
    # print(124)
    return jsonify(listTemplates())

@app.route('/getTemplatePreview', methods=['GET'])
def getTemplatePreview():
    # print(124)
    # get template name in get url
    templateName = request.args.get('templateName', type=str)
    # if no template name provided then tell the user how to get
    # print(templateName)
    if not templateName:
        return jsonify({'🚫 Error': 'no template name specify. trying adding ?templateName=<templateNamehere>'}), 400
    # print(templateName)
    if templateName not in listTemplates():
        return jsonify({'🚫 Error': 'Invalid template name.'}), 400
    # check if template name exists in list of templates
    # then return the file array
    pages = convertToPageImage(os.path.join(outputDir,templateName+'.pdf'))
    # print(pages) 
    # then return the file array
    # convertToPageImage
    return jsonify(pages)

@app.route('/download_template', methods=['GET'])
def download_template():
    template_path = os.path.join(baseDir, 'template.json')

    if not os.path.isfile(template_path):
        return "Template file not found", 404

    return send_file(template_path, as_attachment=True)


@app.route('/create_resume', methods=['POST'])
def create_resume():
    # 0. Receive the data from the frontend
    # print(dir(request))

    # muybe texliveonfly is not able to be accessed by the python env try with out

    # a. Authenticate user (implement your authentication logic here)
    if not athenticateUser(request):
        return "Authentication failed!", 401

    # print(request.headers)

    # b. Get the JSON data from the frontend
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({'🚫 Error': 'Invalid content type. Expected JSON.'}), 400

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
        if resume_output_path is not None:    
            print("generated file path", resume_output_path)

            # 2. Send the resume to the frontend in byte format and delete the file from the folder
            try:
                return send_file(resume_output_path, download_name=f'{templateName}.pdf', as_attachment=True)
            finally:
                os.remove(resume_output_path)
        else:
            raise Exception("Resume not generated, internal error")

    except KeyError as e:
        # print(e)
        app.logger.error(e)
        return jsonify({'🚫 Error': f'Invalid data, missing key {e}'}), 422

    except Exception as e:
        app.logger.error(e)
        if "Resume not generated, internal error" in e.__str__():
            return e.__str__(), 500

        # print(e.with_traceback())
        # get only the site url
        url_parts = urlsplit(request.base_url)

        base_url = url_parts.scheme + "://" + 'buildyourreseume.online'
        # print(base_url)
        # if env is debug then show the error
        return jsonify({
            '🚫 Error': f'Invalid content template, Download template from here {base_url}/download_template'
        }), 422


# @app.route('/create_resume_bulk', methods=['POST'])
# def create_resume_bulk():
#     # 0. recieve the data as list
#     # 1. get the json data from the frontend
#     # a. create resume and save in some folder
#     # b. send the resume to the frontend in byte format and delete the file from the folder
#     return "under development", 200
