# create resumes on different templates
import json
from util.utils import getTemplates, listTemplates

if __name__ == '__main__':
    # read the json file template.json
    with open('template.json') as f:
        data = json.load(f)
    # testing for updating the json data in the middle
    # data['basics']['name'] = 'Rahul' # idk just a simple name to test  

    for template in listTemplates():
        templateCall = getTemplates(template)
        if templateCall is not None:
            filePath = templateCall(template+'.pdf', data)
            print(filePath)