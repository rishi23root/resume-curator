# create resumes on different templates
import os 
from constants import outputDir
from resumeFormat.twoColumn import runner as twoColumnRunner

filename2 = '2ColumnResume.pdf'
twoColumnRunner(filename2)
os.system(f'open {os.path.join(outputDir,filename2)}')
