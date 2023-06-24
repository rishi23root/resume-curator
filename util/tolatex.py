# latex code cretor utils
def createLink(url: str, text: str):
    return f"\\href{{{url}}}{{{text}}}"


def createSection(title: str, content: str):
    return f"""
    \\section{{{title}}}
    {content}
    \\sectionsep
    """


def inBlock(blockName: str, argStr: str):
    return f"\{blockName}{argStr}"


# wrapper which will take arguments and closing element name
# ex - {minipage}[t]{0.66\textwidth}

def latexBlock(blockName: str, argStr: str,endingStr:str="") -> callable:
    starting = f"\{blockName}{argStr}"
    if blockName == "section" and endingStr == "":
        endingStr = f"\{blockName}sep"
        
    def wrapper(middle: str) -> str:
        return f"""{starting}\n{middle}\n{endingStr}"""
    
    return wrapper
