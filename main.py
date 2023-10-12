# # create resumes on different templates
import json

from util.baseFunc import useTemplates, listTemplates


production = 0

if __name__ == '__main__' and production == 1:
    # read the json file template.json
    with open('template.json') as f:
        data = json.load(f)
    # testing for updating the json data in the middle
    data['basics']['name'] = 'Rahul' # idk just a simple name to test  

    for template in listTemplates():
        templateCall = useTemplates(template)
        if templateCall is not None:
            filePath = templateCall(template+'.pdf', data)
            print(filePath)
    
    
# single file testing example
if __name__ == '__main__' and production == 0:
    print("testing single file")
    with open('template.json', 'r') as f:
        data = json.load(f)
        
    templateCall = useTemplates('singleColumn')
    # templateCall = useTemplates('twoColumn')
    filePath = templateCall('testing.pdf', data)
