# create resumes on different templates
import os 
from constants import outputDir
from resumeFormat.twoColumn import runner as twoColumnRunner
from resumeFormat.singleColumn import runner as singleColumnRunner


# first check for possible updates from linkedin and update the json file
# update the json file with latest linkedin data 
# update the json file with latest github data 

filename1 = '1ColumnResume.pdf'
filename2 = '2ColumnResume.pdf'

# 1 column resume
singleColumnRunner(filename1)

# 2 column resume
# twoColumnRunner(filename2)

# os.system(f'open {os.path.join(outputDir,filename2)}')
