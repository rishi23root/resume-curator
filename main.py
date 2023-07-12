# create resumes on different templates
import json
from resumeFormat.twoColumn import runner as twoColumnRunner
from resumeFormat.singleColumn import runner as singleColumnRunner
a
if __name__ == '__main__':
    filename1 = '1ColumnResume.pdf'
    filename2 = '2ColumnResume.pdf'

    # read the json file template.json
    with open('template.json') as f:
        data = json.load(f)

    # testing for updating the json data in the middle
    data['basics']['name'] = 'Rahul'
    filePath = singleColumnRunner(filename1, data)
    print(filePath)
    filePath2 = twoColumnRunner(filename2, data)
    print(filePath2)