# load the file and read the file
# extract just text from the pdf file
# load a pre-trained model to parse the data and return in JSON format (expecting all the fields to be present, all unprocessed fields are left empty)
# if not (3) then fill the JSON with the remaining missing fields
# return the data
import os
import PyPDF2

# read a pdf file from the output folder
pdfFile = open(os.path.join("output", "singleColumn.pdf"), "rb")

# extract all text from pdfFile

pdfReader = PyPDF2.PdfReader(pdfFile)
pdfText = " ".join([ page.extract_text() for page in pdfReader.pages])

# all extracted text
print(pdfText)


