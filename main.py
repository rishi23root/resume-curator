# create resumes on different templates
import os 
from constants import outputDir
from resumeFormat.twoColumn import runner as twoColumnRunner


# first check for possible updates from linkedin and update the json file


# 1 column resume

# 2 column resume

filename2 = '2ColumnResume.pdf'
twoColumnRunner(filename2)
# os.system(f'open {os.path.join(outputDir,filename2)}')
