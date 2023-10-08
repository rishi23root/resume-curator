# take control of the templatet classes 
# create resume.tex file from the data in json provided 
import os

import pylatex as lt

from util.constants import buildDir
from util.utils import createResume


class Template(lt.Document):
    def __init__(self):
        super().__init__(documentclass='resumecustom',
                         page_numbers=False,
                         document_options={},
                         fontenc=None, # type: ignore
                         lmodern=False,
                         textcomp=False,
                         microtype=False)

        # self.preamble.append(lt.Command('title', 'Rishi23root resume builder'))
        # self.preamble.append(lt.Command('author', 'Rishi23root'))
        # self.preamble.append(lt.Command('date', NoEscape(r'\today')))
        # self.append(NoEscape(r'\maketitle'))
        self.jsonData = {}

        # setup for base data
        self.change_document_style("fancy")
        self.remove(lt.Command("pagestyle", arguments=["empty"]))
        self.remove(lt.Command("normalsize"))
        self.packages.remove(lt.Package("inputenc", options=["utf8"]))
        # adding imp packages to start the document
        self.packages.append(lt.Package('fancyhdr'))
        self.append(lt.Command("fancyhf", arguments=[""]))

    def fill_document(self):
        pass

    @classmethod
    def run(cls,filename: str = 'resume.pdf', jsonData: dict = None): # type: ignore
        # get the file name to use 
        name = filename.split('.')[0]
        
        # initialize the class execution
        doc = cls()
        
        # extract data and pass it to the constructor
        if jsonData: doc.jsonData = jsonData
        else: raise Exception("Data is required to build a teamplate")
            
        # Call function to decorate the template with data
        doc.fill_document()

        # # doc.generate_pdf(clean_tex=False)
        doc.generate_tex(filepath=os.path.join(buildDir, name))

        return createResume(filename)