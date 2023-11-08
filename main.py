# # create resumes on different templates
import json

from util.baseFunc import useTemplates, listTemplates


# colored text function 
def prCyan(skk): 
    return "\033[96m {}\033[00m" .format(skk)

production = 1

    
# single file testing example
if __name__ == '__main__' and production == 0:
    print("testing single file")
    with open('template.json', 'r') as f:
        data = json.load(f)
        
    templateCall = useTemplates('singleColumn')
    # templateCall = useTemplates('twoColumn')
    filePath = templateCall('testing.pdf', data)


if __name__ == '__main__' and production == 1:
    # read the json file template.json
    with open('template.json') as f: # type: ignore
        data = json.load(f)
    # testing for updating the json data in the middle
    data['basics']['name'] = 'no one knows' # idk just a simple name to test  

    for template in listTemplates():
        templateCall = useTemplates(template)
        if templateCall is not None:
            print("Using :",prCyan(template.capitalize()),end=' | ')
            filePath = templateCall(template+'.pdf', data)
            print("template, saved at :",prCyan(filePath))
    
