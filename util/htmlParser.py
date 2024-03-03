from bs4 import BeautifulSoup
from pprint import pprint 
import re

pattern = re.compile(r'(?<!\\)%')


def getListItems(html):
    parser = BeautifulSoup(html, 'lxml')
    textList = [tag.text for tag in parser.find_all('li')]
    
    # fix all the formatting issues like \n, \t, \r and %
    textList = [pattern.sub(r"\%",text) for text in textList]
    
    
    return textList
    
    

if __name__ == "__main__":

    data = "<ul><li>\\% Use my extensive experience with front end development to define the structure and components for the project, making sure they are reusable</li><li>Keep the code quality high reviewing code from other developers and suggesting improvements</li><li> Interact with the designer to suggest changes and to make sure the view he has about the design is translated into actual functionality</li><li> E-commerce maintenance <strong>with Fastcommerce</strong>, a Brazilian e-commerce platform</li></ul>"
    r= getListItems(data)
    pprint(r)