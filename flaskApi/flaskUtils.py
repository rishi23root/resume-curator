# flask base api to generate resume form the data recieved from the frontend
# tasks
# 0. recieve the data from the frontend
# a. authenticate user
# b. get the json data from the frontend
# 1. create resume and save in some folder
# 2. send the resume to the frontend in byte format and delete the file from the folder

import base64
import os
import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image

from util.baseFunc import read_json_file, useTemplates
from util.constants import baseDir


def athenticateUser(request):
    # all the authentication code will be handeled by the next-backend
    return True


def generateResume(data: dict, templateName: str) -> Path or None: # type: ignore
    # file name to save the resume
    # return full path of the resume with the file name
    fileName = str(uuid.uuid4()) + '.pdf'

    # get the template and call the function
    templateCall = useTemplates(templateName)
    if templateCall is not None:
        return templateCall(fileName, data)
    else:
        return None # type: ignore


def varifyData(data: dict) :
    # varify the data
    if data is None:
        return False, "data is None"
    # read the json file and varify the data
    templateData = read_json_file(os.path.join(baseDir, 'template.json'))
    for field in templateData.keys():
        # level1
        if field not in data.keys():
            return False, field

        if isinstance(templateData[field], dict):
            for i in templateData[field].keys():
                # level2
                if i not in data[field].keys():
                    return False, '.'.join([field, i])
        else:
            # list
            # select the first element from the list
            example = templateData[field][0]
            for eachElementInList in data[field]:
                for eachField in example.keys():
                    if eachField not in eachElementInList.keys():
                        return False, '.'.join([field, eachField])
    return True, ""


def compress_base64_image(image_string, quality=30):
    # get only base64 part
    if image_string.count(';base64,') == 0:
        return 422, image_string
    glans ,input_base64 = image_string.split(';base64,')
    try:
        # Decode base64 string to bytes
        image_data = base64.b64decode(input_base64)

        # Open image from bytes
        img = Image.open(BytesIO(image_data))

        # Create a BytesIO object to store compressed image
        compressed_img_io = BytesIO()

        # Save the image with specified quality to BytesIO
        img.save(compressed_img_io, format='JPEG', quality=quality, optimize=True)

        # Get the compressed image data as bytes
        compressed_img_data = compressed_img_io.getvalue()

        # Encode the compressed image bytes to base64
        compressed_base64 = base64.b64encode(compressed_img_data).decode('utf-8')

        return 200, glans.replace('png','jpg') + ';base64,' + compressed_base64

    except Exception as e:
        print('[error] ',e)
        return 422, image_string
